AGENT_TOOLS = [
    {
        "type": "function",
        "name": "get_expense",
        "description": "Retrieve an employee expense by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "expense_id": {
                    "type": "integer",
                    "description": "The expense record ID."
                }
            },
            "required": ["expense_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "get_policy",
        "description": "Retrieve the company expense limit for a category.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["meals", "travel", "lodging", "supplies"]
                }
            },
            "required": ["category"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "simulate_payment",
        "description": (
            "Record a simulated reimbursement payment for an expense. "
            "LAB ONLY: No real money is transferred."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expense_id": {
                    "type": "integer",
                    "description": "The expense to reimburse."
                }
            },
            "required": ["expense_id"],
            "additionalProperties": False
        },
        "strict": True
    }
]
