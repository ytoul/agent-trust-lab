import os

from dotenv import load_dotenv
from openai import OpenAI

# Explicit path avoids errors when executing Python via stdin.
load_dotenv(dotenv_path=".env")

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def analyze_expense(description: str) -> str:
    """
    First LLM connectivity test.

    No tools, database access, or payment capabilities.
    """

    client = OpenAI(timeout=30.0, max_retries=0)

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are an expense analysis assistant in an "
            "educational lab. Analyze the provided description "
            "and identify its likely expense category. "
            "Do not approve payments or claim to have accessed "
            "company policies. Keep your response brief."
        ),
        input=description,
        max_output_tokens=200,
        store=False,
    )

    return response.output_text
