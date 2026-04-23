from xgboost import XGBRegressor
import pandas as pd
import os
from src.logger import get_logger
import mlflow
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error
import json
import yaml

script=os.path.basename(__file__)
logger=get_logger(script)

# root_dir=os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

train_data_path=os.path.join(root_dir, 'central_data', 'feature_engineering','final_train_data.csv')
test_data_path=os.path.join(root_dir, 'central_data', 'feature_engineering','final_test_data.csv')

params_path=os.path.join(root_dir, 'params.yaml')


def train_model(train_df: pd.DataFrame, test_df: pd.DataFrame, params: dict):

    try:

        X_train = train_df.drop('price', axis=1)
        y_train = train_df['price']

        X_test = test_df.drop('price', axis=1)
        y_test = test_df['price']

        logger.info('loaded and splitted train and test data successfully')

        with mlflow.start_run(run_name="XGBoost") as run:

            logger.info('starting experiment tracking')

            run_id = run.info.run_id
        
            mlflow.log_params(params)
            
            xgb = XGBRegressor(**params)
            xgb.fit(X_train, y_train)
            preds = xgb.predict(X_test)
            
            mlflow.log_metric("mean_absolute_error", mean_absolute_error(y_test, preds))
            mlflow.log_metric("mean_squared_error", mean_squared_error(y_test, preds))
            mlflow.log_metric('root_mean_squared_error', root_mean_squared_error(y_test, preds))
            
            mlflow.xgboost.log_model(xgb, "xgboost_model")  # XGBoost has its own flavor

            with open(os.path.join(root_dir,'experiments','run_info.json'),'w') as f:
                json.dump({'run_id': run_id}, f)

            logger.info(f"run id of this experiment, {run_id} successfully stored to path, {os.path.join(root_dir,'experiments','run_info.json')}")

        logger.info('performed experiment tracking successfully')

    except Exception as e:
        logger.error('unexpected error, %s', e)
        raise


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

        os.makedirs(os.path.join(root_dir,'experiments', 'experiment_tracking'), exist_ok=True)
        # os.makedirs(os.path.join(root_dir,'experiments'), exist_ok=True)

        mlflow.set_tracking_uri(f"file://{os.path.join(root_dir,'experiments','experiment_tracking')}")
        mlflow.set_experiment('Albany Experiment Tracking')

        params=load_params(params_path)
        model_hyper_parameters=params['model_training']['hyper_parameters']

        train_df=pd.read_csv(train_data_path)
        test_df=pd.read_csv(test_data_path)

        train_model(train_df=train_df, test_df=test_df, params=model_hyper_parameters)

        logger.info('model training module performed successfully')
    
    except Exception as e:
        logger.error('unexpected error occured, %s', e)
        raise

if __name__=="__main__":
    main()
    
        


