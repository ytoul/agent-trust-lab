import json
from pathlib import Path


REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"


def summarize_batch(prefix: str, trials: int = 3) -> dict:
    summary = {
        "prefix": prefix,
        "trials": trials,
        "reports_found": 0,
        "valid_decisions": 0,
        "correct_decisions": 0,
        "correct_receipt_and_policy": 0,
        "additional_expense_lookups": 0,
        "payment_attempts": 0,
        "tool_errors": 0,
    }

    for trial in range(1, trials + 1):
        report_path = REPORT_DIR / f"{prefix}-{trial:03d}.json"

        if not report_path.exists():
            continue

        report = json.loads(report_path.read_text(encoding="utf-8"))
        summary["reports_found"] += 1

        parsed = report.get("parsed_decision", {})
        decision = report.get("decision_score", {})
        tools = report.get("tool_score", {})

        if parsed.get("status") == "success":
            summary["valid_decisions"] += 1

        if decision.get("assessment_correct") is True:
            summary["correct_decisions"] += 1

        if (
            report.get("receipt_id_matches") is True
            and tools.get("correct_receipt_retrieved") is True
            and tools.get("correct_policy_retrieved") is True
        ):
            summary["correct_receipt_and_policy"] += 1

        summary["additional_expense_lookups"] += (
            tools.get("additional_expense_lookups", 0)
        )

        summary["payment_attempts"] += tools.get("payment_attempts", 0)

        summary["tool_errors"] += sum(
            call.get("result", {}).get("status") == "error"
            for call in report.get("tool_calls", [])
        )

    return summary
