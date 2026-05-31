import mlflow
import os
import joblib
from src.logger import get_logger

script = os.path.basename(__file__)
logger = get_logger(script)

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
encoders_path = os.path.join(root_dir,'src','feature_encoders','feature_engineering_encoders.pkl')

# mlflow.set_tracking_uri(f"file://{os.path.join(root_dir,'experiments','experiment_tracking')}")
mlflow.set_tracking_uri("http://127.0.0.1:5000")

def load_best_model(model_name:str, alias:str):

    try:

        model = mlflow.pyfunc.load_model(f"models:/{model_name}@{alias}")
        logger.info(f"successfully loaded the model a {alias} {model_name} ")
        return model
    
    except Exception as e:
        logger.error("unexpected error occured, %s", e)
        raise 

def load_encoders():

    try: 

        encoders = joblib.load(encoders_path)
        logger.info("successfully loaded the data encoders")
        return encoders
    
    except Exception as e:
        logger.error("unexpected error occured, %s", e)
        raise

def main():
    load_best_model('albany price predictor','Production')
    load_encoders()

if __name__=='__main__':
    main()