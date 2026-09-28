from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="PocketSmart AI",
    description="Your Smart Budget & Recommendation Engine",
    version="1.0.0"
)

class BudgetRequest(BaseModel):
    user_id: str
    monthly_income: float
    expenses: dict
    savings_goal: float

@app.get("/")
def read_root():
    return {"status": "Online", "project": "PocketSmart AI"}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}

@app.post("/api/v1/recommend-budget")
def recommend_budget(data: BudgetRequest):
    total_expenses = sum(data.expenses.values())
    remaining_balance = data.monthly_income - total_expenses
    
    if remaining_balance < 0:
        recommendation = "Warning: Expenses exceed income!"
    else:
        recommendation = f"Surplus of ₹{remaining_balance}. Allocate to goal."
        
    return {
        "user_id": data.user_id,
        "remaining_balance": remaining_balance,
        "recommendation": recommendation
    }