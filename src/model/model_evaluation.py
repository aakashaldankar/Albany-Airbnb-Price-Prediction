import mlflow
from mlflow.tracking import MlflowClient
import json
import os

model_name='albany price predictor'

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

tracking_uri = f"file://{os.path.join(root_dir, 'experiments', 'experiment_tracking')}"
mlflow.set_tracking_uri(tracking_uri)

client = MlflowClient()

run_id_path = os.path.join(root_dir,'experiments','run_info.json')

with open(run_id_path, 'r') as f:
    run_id=json.load(f)['run_id']

def register_model(run_id: str, model_name: str):

    run = client.get_run(run_id)

    logged_models = client.search_logged_models(
        experiment_ids=[run.info.experiment_id],
        filter_string=f"source_run_id = '{run_id}'")

    if not logged_models:
        raise ValueError(f"No logged model found for run_id: {run_id}")
    
    model_uri=logged_models[0].model_uri
    model_version=mlflow.register_model(model_uri, model_name)
    version=model_version.version

    metrics=run.data.metrics

    return metrics, version

def is_eligible(metrics: json, threshold_metrics: json):

    return (metrics['mean_absolute_error']<threshold_metrics['mean_absolute_error'] and 
            metrics['mean_squared_error']<threshold_metrics['mean_squared_error'] and 
            metrics['root_mean_squared_error']>threshold_metrics['root_mean_squared_error'])

def get_prod_metrics(model_name: str):

    prod_version=client.get_latest_versions(model_name, stages=["Production"])

    if not prod_version:

        print(f" Model {model_name} has no version in production stage")
        return None
    
    prod_run_id=prod_version[0].run_id
    prod_run=client.get_run(prod_run_id)
    return prod_run.data.metrics

def beats_production(new_metrics: json, prod_metrics: json):

    if prod_metrics is None:
        return True

    return (new_metrics['mean_absolute_error']<prod_metrics['mean_absolute_error'] and 
            new_metrics['mean_squared_error']<prod_metrics['mean_squared_error'] and 
            new_metrics['root_mean_squared_error']>prod_metrics['root_mean_squared_error'])

def main():

    threshold_metrics={"mean_absolute_error": 0.3, 
                    "mean_squared_error": 0.3, 
                    "root_mean_squared_error": 0.3}

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












