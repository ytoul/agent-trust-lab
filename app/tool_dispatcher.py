import json

from app.agent_tools import (
    tool_get_expense,
    tool_get_policy,
    tool_simulate_payment,
)


TOOL_FUNCTIONS = {
    "get_expense": tool_get_expense,
    "get_policy": tool_get_policy,
    "simulate_payment": tool_simulate_payment,
}


def dispatch_tool(tool_name: str, arguments: str) -> dict:
    """
    Execute an allowlisted agent tool.

    INTENTIONAL LAB LIMITATION:
    This dispatcher does not verify user identity,
    expense ownership, or payment authorization.
    """

    if tool_name not in TOOL_FUNCTIONS:
        return {
            "status": "error",
            "reason": f"Unknown tool: {tool_name}",
        }

    try:
        parsed_arguments = json.loads(arguments)
    except json.JSONDecodeError:
        return {
            "status": "error",
            "reason": "Invalid JSON arguments",
        }

    if not isinstance(parsed_arguments, dict):
        return {
            "status": "error",
            "reason": "Tool arguments must be a JSON object",
        }

    try:
        return TOOL_FUNCTIONS[tool_name](**parsed_arguments)
    except (TypeError, ValueError) as error:
        return {
            "status": "error",
            "reason": f"Invalid tool arguments: {error}",
        }
