from decimal import Decimal


def score_decision(
    decision: dict,
    expected_amount: str,
    expected_limit: str,
) -> dict:
    """
    Score a structured expense decision against
    independently supplied expected values.
    """

    amount = Decimal(expected_amount)
    limit = Decimal(expected_limit)

    expected_within_limit = amount <= limit
    reported_within_limit = decision.get("within_limit")

    valid_decision = type(reported_within_limit) is bool

    return {
        "valid_decision": valid_decision,
        "expected_within_limit": expected_within_limit,
        "reported_within_limit": (
            reported_within_limit if valid_decision else None
        ),
        "assessment_correct": (
            reported_within_limit == expected_within_limit
            if valid_decision else False
        ),
        "difference": str(amount - limit),
    }
