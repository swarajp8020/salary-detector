import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.services.parser_service import load_transactions, group_by_customer
from app.services.salary_detector import detect_salary_account
from app.services.scenario_engine import classify_scenario, detect_salary_stopped

# transactions = load_transactions("data/sample_transactions.csv")
transactions = load_transactions("data/test_scenarios.csv")
customer_map = group_by_customer(transactions)

for customer_id, txns in customer_map.items():

    result = detect_salary_account(txns)

    if result["is_salary_account"]:
        scenario = classify_scenario(txns, result["details"])
        churn = detect_salary_stopped(result["details"], txns)
    else:
        scenario = "NON_SALARY"
        churn = False

    print(f"\nCustomer: {customer_id}")
    print({
        **result,
        "scenario": scenario,
        "salary_stopped": churn
    })