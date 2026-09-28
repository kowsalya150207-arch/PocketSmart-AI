from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="PocketSmart AI",
    description="Modular Architecture & API Setup",
    version="1.0.0"
)

class BudgetRequest(BaseModel):
    user_id: str
    monthly_income: float
    expenses: dict
    savings_goal: float

@app.get("/")
def read_root():
    return {"message": "Welcome to PocketSmart AI API Modular Setup!"}

@app.get("/api/v1/status")
def get_status():
    return {"status": "Active", "module": "FastAPI Initialization"}

@app.post("/api/v1/analyze-expense")
def analyze_expense(data: BudgetRequest):
    total_expenses = sum(data.expenses.values())
    remaining_balance = data.monthly_income - total_expenses
    
    return {
        "user_id": data.user_id,
        "total_income": data.monthly_income,
        "total_expenses": total_expenses,
        "remaining_balance": remaining_balance,
        "status": "Success"
    }