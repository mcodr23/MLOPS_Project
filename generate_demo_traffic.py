import requests
import time
import os

url_base = "http://localhost:8005"

def generate_traffic():
    print("Generating demo traffic for Grafana...")
    
    # 1. Hit index
    for _ in range(5):
        requests.get(f"{url_base}/")
        time.sleep(0.1)

    # 2. Hit prediction_ui
    params = {
        'Gender': 'Male', 'Married': 'Yes', 'Dependents': '0', 'Education': 'Graduate', 
        'Self_Employed': 'No', 'ApplicantIncome': 5000, 'CoapplicantIncome': 2000, 
        'LoanAmount': 150, 'Loan_Amount_Term': 360, 'Credit_History': 1, 'Property_Area': 'Urban'
    }
    for _ in range(10):
        requests.post(f"{url_base}/prediction_ui", params=params)
        time.sleep(0.1)

    # 3. Hit batch_prediction
    test_csv = os.path.join('prediction_model', 'datasets', 'test.csv')
    if os.path.exists(test_csv):
        with open(test_csv, 'rb') as f:
            for _ in range(3):
                f.seek(0)
                requests.post(f"{url_base}/batch_prediction", files={'file': f})
                time.sleep(0.1)

    print("✅ Traffic generation complete.")

if __name__ == "__main__":
    generate_traffic()
