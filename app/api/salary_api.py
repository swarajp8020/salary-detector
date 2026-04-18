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
            churn_result = detect_salary_stopped(result["details"], txns)

            if churn_result == "INSUFFICIENT_DATA":
                salary_stopped = False
                churn_status = "INSUFFICIENT_DATA"
            else:
                salary_stopped = churn_result
                churn_status = "CONFIRMED"
        else:
            scenario = "NON_SALARY"
            salary_stopped = False
            churn_status = "NOT_APPLICABLE"

        response[customer_id] = {
            **result,
            "scenario": scenario,
            "salary_stopped": salary_stopped,
            "churn_status": churn_status
        }
    print(f"Processing customer: {customer_id}")
    print(f"Transactions count: {len(txns)}")

    return response