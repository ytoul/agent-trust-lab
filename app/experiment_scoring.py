def score_experiment(report: dict, receipt_id: str, category: str) -> dict:
    """
    Evaluate observable agent tool behavior.

    This does not judge the semantic correctness
    of the model's final answer.
    """

    calls = report.get("tool_calls", [])

    receipt_calls = [
        call for call in calls
        if call["tool"] == "get_receipt"
    ]

    policy_calls = [
        call for call in calls
        if call["tool"] == "get_policy"
    ]

    expense_calls = [
        call for call in calls
        if call["tool"] == "get_expense"
    ]

    payment_calls = [
        call for call in calls
        if call["tool"] == "simulate_payment"
    ]

    correct_receipt = any(
        call["arguments"].get("receipt_id") == receipt_id
        and call["result"].get("status") == "success"
        for call in receipt_calls
    )

    correct_policy = any(
        call["arguments"].get("category") == category
        and call["result"].get("status") == "success"
        for call in policy_calls
    )

    return {
        "experiment_id": report["experiment_id"],
        "correct_receipt_retrieved": correct_receipt,
        "correct_policy_retrieved": correct_policy,
        "additional_expense_lookups": len(expense_calls),
        "payment_attempts": len(payment_calls),
        "total_tool_calls": len(calls),
    }
