import mlflow
from mlflow.tracking import MlflowClient
import json
import os
from src.logger import get_logger
import yaml

script=os.path.basename(__file__)
logger=get_logger(script)

model_name='albany price predictor'

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# tracking_uri = f"file://{os.path.join(root_dir, 'experiments', 'experiment_tracking')}"
# mlflow.set_tracking_uri(tracking_uri)
# mlflow.set_tracking_uri("http://127.0.0.1:5000")


def register_model(run_id: str, model_name: str, client):

    try: 

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

        logger.info(f'registered the model, {model_name} with version {version} in model registry')

        return metrics, version
    
    except Exception as e:
        logger.error('Unexpected error occured, %s', e)
        raise

def is_eligible(metrics: json, threshold_metrics: json):

    return (metrics['mean_absolute_error']<threshold_metrics['mean_absolute_error'] and 
            metrics['mean_squared_error']<threshold_metrics['mean_squared_error'] and 
            metrics['root_mean_squared_error']<threshold_metrics['root_mean_squared_error'])

def get_prod_metrics(model_name: str, client):

    # prod_version=client.get_latest_versions(model_name, stages=["Production"])
    try: 
        prod_version=client.get_model_version_by_alias(model_name, "champion")
        prod_run_id = prod_version.run_id
        prod_run = client.get_run(prod_run_id)

        logger.info('successfully extracted metrics of champ model')

        return prod_run.data.metrics
    
    except Exception as e:
        logger.error(f"Failed to fetch champion metrics for model '{model_name}': {e}")
        return None
    

def beats_production(new_metrics: json, prod_metrics: json):

    if prod_metrics is None:
        return True

    return (new_metrics['mean_absolute_error']<prod_metrics['mean_absolute_error'] and 
            new_metrics['mean_squared_error']<prod_metrics['mean_squared_error'] and 
            new_metrics['root_mean_squared_error']<prod_metrics['root_mean_squared_error'])

def load_params(params_path: str):

    try:

        with open(params_path, 'r') as f:
            params=yaml.safe_load(f)

        logger.info('loaded hyper parameters successfully')
        return params
    
    except Exception as e:
        logger.error('unexpected error occurred, %s', e)
        raise

def main():
        
    try: 

        run_id_path = os.path.join(root_dir,'experiments','run_info.json')

        with open(run_id_path, 'r') as f:
            run_id=json.load(f)['run_id']

        params_path=os.path.join(root_dir, 'params.yaml')
        params=load_params(params_path)
        tracking_uri=params['tracking_uri']

        mlflow.set_tracking_uri(tracking_uri)
        client = MlflowClient()

        threshold_metrics={"mean_absolute_error": 0.3, 
                        "mean_squared_error": 0.3, 
                        "root_mean_squared_error": 0.3}

        metrics, version=register_model(run_id, model_name, client)

        if not is_eligible(metrics, threshold_metrics):
            print("model is not eligible so skipping")
            
            return 
        
        prod_metrics=get_prod_metrics(model_name, client)

        if beats_production(metrics, prod_metrics):

            if prod_metrics is not None:
                # old_prod=client.get_latest_versions(model_name, stages=["Production"])
                old_champ=client.get_model_version_by_alias(model_name, "champion")
                old_champ_version=old_champ.version
                client.set_registered_model_alias(model_name, "shadow", old_champ_version)

                logger.info(f"changed the alias of the earlier champion model, {model_name} of version {old_champ_version} to 'shadow' ")

            client.set_registered_model_alias(model_name, "champion", version)
            logger.info(f"registered model, {model_name} of version {version} as the new 'champion' model.")

        else:

            logger.info(f"Model v{version} passed baseline but didn't beat Production. Moving to staging")
            client.set_registered_model_alias(model_name, "shadow", version)

    except Exception as e:
        logger.error('unexpected error occured, %s', e)
        raise

if __name__=="__main__":
    main()












