from app.experiment_runner import run_experiment


def run_batch(
    prefix: str,
    receipt_id: str,
    amount: str,
    limit: str,
    category: str,
    trials: int = 3,
) -> list[dict]:
    """
    Execute repeated structured expense assessments.

    Each trial creates its own JSON report.
    """

    results = []

    for trial in range(1, trials + 1):
        experiment_id = f"{prefix}-{trial:03d}"

        print(f"\nRunning {experiment_id}")

        result = run_experiment(
            experiment_id=experiment_id,
            question=(
                f"Retrieve receipt {receipt_id} and its applicable "
                "company expense policy. Determine whether it "
                "is within the normal spending limit."
            ),
            structured=True,
            expected_receipt_id=receipt_id,
            expected_category=category,
            expected_amount=amount,
            expected_limit=limit,
        )

        results.append(result)

        parsed = result.get("parsed_decision", {})
        decision_score = result.get("decision_score", {})

        print("Parser:", parsed.get("status"))
        print(
            "Assessment correct:",
            decision_score.get("assessment_correct"),
        )
        print("Tool calls:", result["tool_call_count"])

    return results
