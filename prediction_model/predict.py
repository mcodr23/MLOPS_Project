import pandas as pd
import numpy as np
from prediction_model.config import config  
import mlflow
import os
import glob

mlflow.set_tracking_uri(config.TRACKING_URI)

def load_model_robust(model_uri):
    """Try standard MLflow load, fallback to disk search if it fails."""
    try:
        return mlflow.sklearn.load_model(model_uri)
    except Exception as e:
        print(f"MLflow load failed: {e}. Searching disk...")
        # Search for model.pkl in mlruns recursively
        model_files = glob.glob(os.path.join("mlruns", "**", "model.pkl"), recursive=True)
        if not model_files:
             raise FileNotFoundError("Could not find any model.pkl on disk.")
        
        # Pick the most recent one
        latest_model = max(model_files, key=os.path.getmtime)
        print(f"Found fallback model: {latest_model}")
        import joblib
        return joblib.load(latest_model)

mlflow.set_tracking_uri(config.TRACKING_URI)


def generate_predictions(data_input):
    data = pd.DataFrame(data_input)
    experiment_name = config.EXPERIMENT_NAME
    experiment = mlflow.get_experiment_by_name(experiment_name)
    experiment_id = experiment.experiment_id
    runs_df=mlflow.search_runs(experiment_ids=experiment_id,order_by=['metrics.f1_score DESC'])
    best_run=runs_df.iloc[0]
    best_run_id=best_run['run_id']
    best_model='runs:/' + best_run_id + '/' + config.MODEL_NAME.lstrip('/')
    loan_prediction_model=load_model_robust(best_model)
    prediction=loan_prediction_model.predict(data)
    output = np.where(prediction==1,'Y','N')
    result = {"prediction":output}
    return result


def generate_predictions_batch(data_input):
    # data = pd.DataFrame(data_input)
    experiment_name = config.EXPERIMENT_NAME
    experiment = mlflow.get_experiment_by_name(experiment_name)
    experiment_id = experiment.experiment_id
    runs_df=mlflow.search_runs(experiment_ids=experiment_id,order_by=['metrics.f1_score DESC'])
    best_run=runs_df.iloc[0]
    best_run_id=best_run['run_id']
    best_model='runs:/' + best_run_id + '/' + config.MODEL_NAME.lstrip('/')
    loan_prediction_model=load_model_robust(best_model)
    prediction=loan_prediction_model.predict(data_input)
    output = np.where(prediction==1,'Y','N')
    result = {"prediction":output}
    return result


    


if __name__=='__main__':
    generate_predictions()