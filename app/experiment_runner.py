import io
import json
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from app.decision_parser import parse_decision
from app.decision_scoring import score_decision
from app.experiment_scoring import score_experiment
from app.read_only_agent import ask_expense_agent


REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"


def run_experiment(
    experiment_id: str,
    question: str,
    save_report: bool = True,
    structured: bool = False,
    expected_receipt_id: str | None = None,
    expected_category: str | None = None,
    expected_amount: str | None = None,
    expected_limit: str | None = None,
) -> dict:

    output_buffer = io.StringIO()
    tool_trace = []

    with redirect_stdout(output_buffer):
        answer = ask_expense_agent(
            question,
            trace=tool_trace,
            structured=structured,
        )

    report = {
        "experiment_id": experiment_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "structured": structured,
        "tool_calls": tool_trace,
        "tool_call_count": len(tool_trace),
        "final_answer": answer,
        "console_trace": output_buffer.getvalue(),
    }

    if expected_receipt_id and expected_category:
        report["tool_score"] = score_experiment(
            report,
            receipt_id=expected_receipt_id,
            category=expected_category,
        )

    if structured:
        parsed = parse_decision(answer)
        report["parsed_decision"] = parsed

        if parsed["status"] == "success":
            decision = parsed["decision"]

            if expected_receipt_id is not None:
                report["receipt_id_matches"] = (
                    decision["receipt_id"] == expected_receipt_id
                )

            if expected_amount is not None and expected_limit is not None:
                report["decision_score"] = score_decision(
                    decision,
                    expected_amount=expected_amount,
                    expected_limit=expected_limit,
                )

    if save_report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

        report_path = REPORT_DIR / f"{experiment_id}.json"

        with report_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=2, ensure_ascii=False)

        print(f"Report saved: {report_path}")

    return report
