from fastapi import APIRouter
from app.services.salary_detector import detect_salary_account
from app.services.parser_service import load_transactions, group_by_customer
from app.services.scenario_engine import classify_scenario, detect_salary_stopped

router = APIRouter()

@router.get("/analyze-sample")
def analyze_sample():

    # transactions = load_transactions("data/sample_transactions.csv")
    transactions = load_transactions("data/test_scenarios.csv")
    customer_map = group_by_customer(transactions)

    response = {}

    for customer_id, txns in customer_map.items():

        result = detect_salary_account(txns)

        if result["is_salary_account"]:
            scenario = classify_scenario(txns, result["details"])
            churn = detect_salary_stopped(result["details"], txns)
        else:
            scenario = "NON_SALARY"
            churn = False

        response[customer_id] = {
            **result,
            "scenario": scenario,
            "salary_stopped": churn
        }
    print(f"Processing customer: {customer_id}")
    print(f"Transactions count: {len(txns)}")

    return response