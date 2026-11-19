from decimal import Decimal

from app.models import ExpenseRequest


POLICY_LIMITS = {
    "meals": Decimal("100.00"),
    "travel": Decimal("500.00"),
    "lodging": Decimal("250.00"),
    "supplies": Decimal("200.00"),
}


def evaluate_expense(expense: ExpenseRequest) -> dict:
    limit = POLICY_LIMITS[expense.category]

    if expense.amount > limit:
        return {
            "decision": "rejected",
            "reason": "Expense exceeds category limit",
            "policy_limit": str(limit),
        }

    return {
        "decision": "eligible",
        "reason": "Expense is within category limit",
        "policy_limit": str(limit),
    }
