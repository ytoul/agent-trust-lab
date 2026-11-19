from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.models import ExpenseRequest
from app.policy import evaluate_expense
from app.database import (
    initialize_database,
    save_expense,
    get_expense,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Agent Trust Lab - Expense Agent",
    description="Educational AI expense processing and threat modeling lab",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "application": "expense-agent",
        "version": "0.1.0",
    }


@app.post("/expenses", status_code=201)
def submit_expense(expense: ExpenseRequest):
    policy_result = evaluate_expense(expense)

    expense_id = save_expense(expense, policy_result)

    return {
        "message": "Expense saved and evaluated",
        "expense_id": expense_id,
        "status": "evaluated",
        "expense": expense.model_dump(mode="json"),
        "policy_result": policy_result,
    }


@app.get("/expenses/{expense_id}")
def retrieve_expense(expense_id: int):
    expense = get_expense(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return expense
