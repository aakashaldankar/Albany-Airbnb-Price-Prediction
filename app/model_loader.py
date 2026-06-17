import mlflow
import joblib
import os
from src.logger import get_logger
from mlflow.tracking import MlflowClient
from mlflow.artifacts import download_artifacts

script = os.path.basename(__file__)
logger = get_logger(script)

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# encoders_path = os.path.join(root_dir,'src','feature_encoders','feature_engineering_encoders.pkl')

# mlflow.set_tracking_uri(f"file://{os.path.join(root_dir,'experiments','experiment_tracking')}")
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))

def load_best_model(model_name:str, alias:str):

    try:

        model = mlflow.pyfunc.load_model(f"models:/{model_name}@{alias}")
        logger.info(f"successfully loaded {alias} {model_name} model")
        return model
    
    except Exception as e:
        logger.error("unexpected error occured, %s", e)
        raise 

def load_encoders(model_name: str, alias: str):

    try: 

        client = MlflowClient()

        model_version=client.get_model_version_by_alias(model_name, alias)
        encoder_file=download_artifacts(artifact_uri=(f"runs:/{model_version.run_id}/feature_engineering/feature_engineering_encoders.pkl"))

        encoders = joblib.load(encoder_file)
        logger.info("successfully loaded the data encoders")
        return encoders
    
    except Exception as e:
        logger.error("unexpected error occured, %s", e)
        raise

def main():
    model_name = os.getenv("MODEL_NAME", "albany price predictor")
    model_alias = os.getenv("MODEL_ALIAS", "champion")
    load_best_model(model_name, model_alias)
    load_encoders()

if __name__=='__main__':
    main()
