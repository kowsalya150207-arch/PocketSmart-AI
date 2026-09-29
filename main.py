import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(
    title="PocketSmart AI",
    description="Smart Budget & Gemini API Recommendation Engine",
    version="1.0.0"
)

# Gemini API Configuration (Replace with valid API Key if needed)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class BudgetInput(BaseModel):
    user_id: str
    monthly_income: float
    expenses: dict  # e.g., {"rent": 10000, "food": 5000, "travel": 2000}
    savings_goal: float

@app.get("/")
def read_root():
    return {"message": "Welcome to PocketSmart AI System"}

# Task 1: Route to Validate Gemini API Connectivity
@app.get("/api/v1/test-gemini")
def test_gemini_connection():
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Simple health check prompt
        response = model.generate_content("Hello, reply with 'Gemini API Connected Successfully!'")
        return {"status": "Success", "response": response.text.strip()}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

# Task 2 & 3: Fast API Route to process and test Real-World Budget Inputs
@app.post("/api/v1/analyze-budget")
def analyze_budget(data: BudgetInput):
    total_expenses = sum(data.expenses.values())
    remaining_balance = data.monthly_income - total_expenses
    
    # Financial assessment status
    if remaining_balance < 0:
        status = "Deficit - Expenses exceed income!"
    elif remaining_balance >= data.savings_goal:
        status = "On Track - Savings Goal Achieved!"
    else:
        status = "Needs Improvement - Below Savings Goal"

    return {
        "user_id": data.data if hasattr(data, 'data') else data.user_id,
        "monthly_income": data.monthly_income,
        "total_expenses": total_expenses,
        "remaining_balance": remaining_balance,
        "savings_goal": data.savings_goal,
        "financial_status": status
    }