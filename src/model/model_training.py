from xgboost import XGBRFRegressor
import pandas as pd
import os
from src.logger import get_logger
import mlflow
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error

script=os.path.basename(__file__)
logger=get_logger(script)

root_dir=os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
train_data_path=os.path.join(root_dir, 'central_data', 'feature_engineering')

def train_model(train_df: pd.DataFrame, test_df: pd.DataFrame, params: dict):

    X_train = train_df.drop('price', axis=1)
    y_train = train_df['price']

    X_test = test_df.drop('price', axis=1)
    y_test = test_df['price']

    with mlflow.start_run(run_name="XGBoost"):
    
        mlflow.log_params(params)
        
        xgb = XGBRFRegressor(**params)
        xgb.fit(X_train, y_train)
        preds = xgb.predict(X_test)
        
        mlflow.log_metric("mean_absolute_error", mean_absolute_error(y_test, preds))
        mlflow.log_metric("mean_squared_error", mean_squared_error(y_test, preds))
        mlflow.log_metric('root_mean_squared_error', root_mean_squared_error(y_test, preds))
        
        mlflow.xgboost.log_model(xgb, "xgboost_model")  # XGBoost has its own flavor




