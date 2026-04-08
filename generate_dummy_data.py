import pandas as pd
import numpy as np
import os

cwd = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(cwd, 'prediction_model', 'datasets')

def generate_data(num_samples):
    np.random.seed(42)
    data = {
        'Gender': np.random.choice(['Male', 'Female'], num_samples),
        'Married': np.random.choice(['Yes', 'No'], num_samples),
        'Dependents': np.random.choice(['0', '1', '2', '3+'], num_samples),
        'Education': np.random.choice(['Graduate', 'Not Graduate'], num_samples),
        'Self_Employed': np.random.choice(['Yes', 'No'], num_samples),
        'ApplicantIncome': np.random.uniform(1000, 10000, num_samples),
        'CoapplicantIncome': np.random.uniform(0, 5000, num_samples),
        'LoanAmount': np.random.uniform(50, 500, num_samples),
        'Loan_Amount_Term': np.random.choice([120, 240, 360, 480], num_samples),
        'Credit_History': np.random.choice([0.0, 1.0], num_samples),
        'Property_Area': np.random.choice(['Urban', 'Rural', 'Semiurban'], num_samples),
        'Loan_Status': np.random.choice(['Y', 'N'], num_samples)
    }
    return pd.DataFrame(data)

os.makedirs(dataset_dir, exist_ok=True)

train_df = generate_data(500)
test_df = generate_data(100)
test_df.drop('Loan_Status', axis=1, inplace=True) # test doesn't need target usually, but let's see. Wait, in config.py, test.csv is it labeled?
# The code doesn't load test.csv target usually in test metrics. Actually training_pipeline uses train_test_split.
# Let's add Loan_Status to test.csv anyway just in case the system expects it.
test_df['Loan_Status'] = np.random.choice(['Y', 'N'], 100)

train_df.to_csv(os.path.join(dataset_dir, 'train.csv'), index=False)
test_df.to_csv(os.path.join(dataset_dir, 'test.csv'), index=False)

print("Dummy data generated successfully.")
