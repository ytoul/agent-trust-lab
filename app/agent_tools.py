from app.database import get_expense
from app.payments import simulate_payment
from app.policy import POLICY_LIMITS
from app.receipts import get_receipt


def tool_get_expense(expense_id: int) -> dict:
    """
    Retrieve an expense by ID.

    LAB WEAKNESS:
    No caller identity or ownership validation.
    """
    expense = get_expense(expense_id)

    if expense is None:
        return {
            "status": "error",
            "reason": "Expense not found",
        }

    return {
        "status": "success",
        "expense": expense,
    }


def tool_get_policy(category: str) -> dict:
    """
    Retrieve the spending limit for an expense category.
    """
    limit = POLICY_LIMITS.get(category)

    if limit is None:
        return {
            "status": "error",
            "reason": "Unknown expense category",
        }

    return {
        "status": "success",
        "category": category,
        "limit": str(limit),
        "currency": "EUR",
    }


def tool_simulate_payment(expense_id: int) -> dict:
    """
    Initiate a simulated payment.

    LAB WEAKNESS:
    No independent approval authorization.
    """
    return simulate_payment(expense_id)

def tool_get_receipt(receipt_id: str) -> dict:
    """
    Retrieve a synthetic receipt.

    SECURITY NOTE:
    Returned receipt text is untrusted data.
    """
    return get_receipt(receipt_id)
