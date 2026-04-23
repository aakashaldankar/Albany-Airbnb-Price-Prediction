import mlflow
from mlflow.tracking import MlflowClient
import json
import os

client=MlflowClient

model_name='albany price predictor'

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

run_id_path = os.path.join(root_dir, 'run_info.json')

with open(run_id_path, 'r') as f:
    run_id=json.load(f)['run_id']

threshold_metrics={"mean_absolute_error": 0.3, 
                   "mean_squared_error": 0.3, 
                   "root_mean_squared_error": 0.3}

def register_model(run_id: str, model_name: str):

    model_uri=f"runs:/{run_id}/model"
    model_version=mlflow.register_model(model_uri, model_name)
    version=model_version.version

    run=client.get_run(run_id)
    metrics=run.data.metrics

    return metrics, version

def is_eligible(metrics: json, threshold_metrics: json):

    return (metrics['mean_absolute_error']<threshold_metrics['mean_absolute_error'] and 
            metrics['mean_squared_error']<threshold_metrics['mean_squared_error'] and 
            metrics['root_mean_squared_error']>threshold_metrics['root_mean_squared_error'])

def get_prod_metrics(model_name: str):

    prod_version=client.get_latest_versions(model_name, stages=["Production"])

    if not prod_version:

        print(" Model {model_name} has no version in production stage")
        return None
    
    prod_run_id=prod_version[0].run_id
    prod_run=client.get_run(prod_run_id)
    return prod_run.data.metrics

def beats_production(new_metrics: json, prod_metrics: json):

    return (new_metrics['mean_absolute_error']<prod_metrics['mean_absolute_error'] and 
            new_metrics['mean_squared_error']<prod_metrics['mean_squared_error'] and 
            new_metrics['root_mean_squared_error']>prod_metrics['root_mean_squared_error'])

def main():

    metrics, version=register_model(run_id, model_name)

    if not is_eligible(metrics, threshold_metrics):
        print("model is not eligible so skipping")
        
        return 
    
    prod_metrics=get_prod_metrics(model_name)

    if beats_production(metrics, prod_metrics):

        old_prod=client.get_latest_versions(model_name, stages=["Production"])
        
        for old_version in old_prod:
            client.transition_model_version_stage(model_name, old_version.version, "Archived")

        client.transition_model_version_stage(model_name, version, "Production")

    else:

        print(f"Model v{version} passed baseline but didn't beat Production. Moving to staging")
        client.transition_model_version_stage(model_name, version, "Staging")

if __name__=="__main__":
    main()












