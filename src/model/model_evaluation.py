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

def get_latest_trained_metrics(model_name: str, client):

    try: 
        latest_trained_version=client.get_model_version_by_alias(model_name, 'latest_trained')

        latest_trained_run_id=latest_trained_version.run_id
        latest_trained_run=client.get_run(latest_trained_run_id)

        metrics=latest_trained_run.data.metrics
        version=latest_trained_version.version

        logger.info(f"successfully extracted metrics of latest_trained model version {version}")

        return metrics, version
    
    except Exception as e:
        logger.error(f"Failed to fetch latest_trained metrics for model {model_name}: {e}")

def is_eligible(metrics: json, threshold_metrics: json):

    return (metrics['mean_absolute_error']<threshold_metrics['mean_absolute_error'] and 
            metrics['mean_squared_error']<threshold_metrics['mean_squared_error'] and 
            metrics['root_mean_squared_error']<threshold_metrics['root_mean_squared_error'])

def get_prod_metrics(model_name: str, client):

    try: 
        prod_version=client.get_model_version_by_alias(model_name, "champion")
        prod_run_id = prod_version.run_id
        prod_run = client.get_run(prod_run_id)

        logger.info('successfully extracted metrics of champ model')

        return prod_run.data.metrics
    
    except Exception as e:
        logger.warning(f"No champion model found for {model_name}. This is expected on the first model evaluation run. {e} ")
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

        params_path=os.path.join(root_dir, 'params.yaml')
        params=load_params(params_path)
        tracking_uri=os.getenv(params['tracking_uri'],'MLFLOW_TRACKING_URI')

        mlflow.set_tracking_uri(tracking_uri)
        client = MlflowClient()

        threshold_metrics={"mean_absolute_error": 0.5, 
                        "mean_squared_error": 0.5, 
                        "root_mean_squared_error": 0.5}

        metrics, version = get_latest_trained_metrics(model_name, client)

        if not is_eligible(metrics, threshold_metrics):
            print("This latest trained model is not eligible so skipping.")
            return 
        
        prod_metrics=get_prod_metrics(model_name, client)

        if beats_production(metrics, prod_metrics):

            if isinstance(prod_metrics, dict):

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











