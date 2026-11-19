import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "expenses.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id TEXT NOT NULL,
                merchant TEXT NOT NULL,
                amount TEXT NOT NULL,
                currency TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                policy_decision TEXT NOT NULL,
                policy_reason TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'evaluated',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER NOT NULL UNIQUE,
                employee_id TEXT NOT NULL,
                amount TEXT NOT NULL,
                currency TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'simulated',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (expense_id) REFERENCES expenses(id)
            )
            """)
def save_expense(expense, policy_result):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO expenses (
                employee_id, merchant, amount, currency,
                category, description, policy_decision,
                policy_reason, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                expense.employee_id,
                expense.merchant,
                str(expense.amount),
                expense.currency,
                expense.category,
                expense.description,
                policy_result["decision"],
                policy_result["reason"],
                "evaluated",
            ),
        )

        return cursor.lastrowid


def get_expense(expense_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM expenses WHERE id = ?",
            (expense_id,),
        ).fetchone()

        return dict(row) if row else None