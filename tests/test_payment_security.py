import json

import app.database as database
from app.models import ExpenseRequest
from app.policy import evaluate_expense
from app.tool_dispatcher import dispatch_tool


def test_payment_without_independent_approval(tmp_path, monkeypatch):
    """
    INTENTIONALLY VULNERABLE BASELINE.

    Demonstrates that an eligible expense can be paid
    without independent approval.

    Uses an isolated temporary SQLite database.
    """

    test_db = tmp_path / "test_expenses.db"
    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.initialize_database()

    expense = ExpenseRequest(
        employee_id="EMP001",
        merchant="Athens Hotel",
        amount="85.00",
        currency="EUR",
        category="meals",
        description="Client dinner",
    )

    policy_result = evaluate_expense(expense)
    expense_id = database.save_expense(expense, policy_result)

    result = dispatch_tool(
        "simulate_payment",
        json.dumps({"expense_id": expense_id}),
    )

    # VULNERABILITY: Payment succeeds without approval.
    assert result["status"] == "simulated"

    saved_expense = database.get_expense(expense_id)
    assert saved_expense["status"] == "paid"

    with database.get_connection() as connection:
        payment = connection.execute(
            "SELECT * FROM payments WHERE expense_id = ?",
            (expense_id,),
        ).fetchone()

    assert payment is not None
    assert payment["amount"] == "85.00"
