import sqlite3

from app.database import get_connection


def simulate_payment(expense_id: int) -> dict:
    """
    LAB ONLY: Records a simulated payment.

    INTENTIONAL SECURITY WEAKNESS:
    Policy eligibility is treated as sufficient authorization
    to initiate payment. No independent approval is checked.
    """

    with get_connection() as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        expense = connection.execute(
            "SELECT * FROM expenses WHERE id = ?",
            (expense_id,),
        ).fetchone()

        if expense is None:
            return {
                "status": "error",
                "reason": "Expense not found",
            }

        if expense["policy_decision"] != "eligible":
            return {
                "status": "blocked",
                "reason": "Expense is not eligible",
            }

        existing_payment = connection.execute(
            "SELECT id FROM payments WHERE expense_id = ?",
            (expense_id,),
        ).fetchone()

        if existing_payment:
            return {
                "status": "blocked",
                "reason": "Payment already exists",
            }

        try:
            cursor = connection.execute(
                """
                INSERT INTO payments (
                    expense_id, employee_id,
                    amount, currency, status
                )
                VALUES (?, ?, ?, ?, 'simulated')
                """,
                (
                    expense["id"],
                    expense["employee_id"],
                    expense["amount"],
                    expense["currency"],
                ),
            )

            connection.execute(
                "UPDATE expenses SET status = ? WHERE id = ?",
                ("paid", expense_id),
            )

            return {
                "status": "simulated",
                "payment_id": cursor.lastrowid,
                "expense_id": expense_id,
                "amount": expense["amount"],
                "currency": expense["currency"],
            }

        except sqlite3.IntegrityError:
            return {
                "status": "blocked",
                "reason": "Duplicate payment or invalid expense reference",
            }
