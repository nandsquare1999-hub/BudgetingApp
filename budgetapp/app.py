from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from budgetapp.routers import categories, budget, transactions, rollover
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Budgeting API")

# Allow React frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(budget.router, prefix="/budget", tags=["budget"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(rollover.router, prefix="/rollover", tags=["rollover"])

@app.get("/")
def root():
    return {"message": "Budgeting API is running!"}
