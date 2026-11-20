import json
import app.database as database

from app.tool_dispatcher import dispatch_tool


def test_valid_policy_lookup():
    result = dispatch_tool(
        "get_policy",
        json.dumps({"category": "meals"}),
    )

    assert result["status"] == "success"
    assert result["limit"] == "100.00"


def test_unknown_tool_rejected():
    result = dispatch_tool("delete_database", "{}")

    assert result["status"] == "error"
    assert "Unknown tool" in result["reason"]


def test_invalid_json_rejected():
    result = dispatch_tool(
        "get_expense",
        "not valid json",
    )

    assert result["status"] == "error"
    assert result["reason"] == "Invalid JSON arguments"


def test_unknown_expense(tmp_path, monkeypatch):
    # Use an isolated database for this test.
    test_db = tmp_path / "expenses.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    # Create the required tables.
    database.initialize_database()

    # Verify that an unknown expense returns a controlled error.
    result = dispatch_tool(
        "get_expense",
        json.dumps({"expense_id": 999999}),
    )

    assert result["status"] == "error"
    assert result["reason"] == "Expense not found"
