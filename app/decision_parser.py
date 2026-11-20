import json


def parse_decision(text: str) -> dict:
    """
    Parse and validate a structured AI expense decision.

    Reject malformed or incomplete decisions.
    """

    try:
        decision = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {
            "status": "error",
            "reason": "Invalid JSON decision",
        }

    if not isinstance(decision, dict):
        return {
            "status": "error",
            "reason": "Decision must be a JSON object",
        }

    receipt_id = decision.get("receipt_id")
    within_limit = decision.get("within_limit")
    reason = decision.get("reason")

    if not isinstance(receipt_id, str) or not receipt_id.strip():
        return {
            "status": "error",
            "reason": "Missing or invalid receipt_id",
        }

    if type(within_limit) is not bool:
        return {
            "status": "error",
            "reason": "within_limit must be a boolean",
        }

    if not isinstance(reason, str) or not reason.strip():
        return {
            "status": "error",
            "reason": "Missing or invalid reason",
        }

    return {
        "status": "success",
        "decision": {
            "receipt_id": receipt_id,
            "within_limit": within_limit,
            "reason": reason,
        },
    }
