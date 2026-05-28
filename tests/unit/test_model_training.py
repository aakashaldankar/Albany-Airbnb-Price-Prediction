from src.model.model_training import train_model, load_params, main
from contextlib import contextmanager
import os
import mlflow.xgboost
import yaml
import pandas as pd

def test_load_params():

    result=load_params('params.yaml')

    assert "model_training" in result
    assert "hyper_parameters" in result['model_training']

def test_train_model(tmp_path, sample_train_data, monkeypatch):

    train_data, test_data = sample_train_data

    calls={
        "start_run":False,
        "log_params": False,
        "log_metric": 0,
        "log_model":False,
    }

    @contextmanager
    def mock_start_run(*args, **kwargs):
        
        calls["start_run"]=True

        class MockRun:
            
            class info:
                run_id="dummy_run"

        yield MockRun()

    def mock_log_params(*args, **kwargs):
        calls["log_params"]=True

    def mock_log_metric(*args, **kwargs):
        calls["log_metric"]+=1
    
    def mock_log_model(*args, **kwargs):
        calls["log_model"]=True

    monkeypatch.setattr('src.model.model_training.mlflow.start_run',mock_start_run)
    monkeypatch.setattr("src.model.model_training.mlflow.log_params",mock_log_params)
    monkeypatch.setattr("src.model.model_training.mlflow.log_metric",mock_log_metric)
    monkeypatch.setattr("src.model.model_training.mlflow.xgboost.log_model",mock_log_model)
    monkeypatch.setattr("src.model.model_training.root_dir",tmp_path)

    params={"max_depth": 2, "learning_rate": 0.1}

    (tmp_path / "experiments").mkdir()

    train_model(train_data, test_data, params)

    assert calls["log_params"]
    assert calls["log_metric"]==3
    assert calls["start_run"]
    assert calls["log_model"]
    

def test_main(monkeypatch, tmp_path):

    calls={
        "mock_set_tracking": False,
        "set_experiment": False,
        "train_model": False,
        "read_csv": 0
    }

    def mock_set_tracking_uri(uri):

        calls["mock_set_tracking"]=True
        assert uri=="http://127.0.0.1:5001"

    def mock_set_experiment(name):

        calls["set_experiment"]=True
        assert name=='Albany Experiment Tracking'

    def mock_train_model(train_df, test_df, params):

        calls["train_model"]=True
        assert train_df.shape[0]==3
        assert test_df.shape[1]==2
        assert params=={'learning_rate': 0.1, 'max_depth': 6, 'n_estimators': 200, 'subsample': 0.8}

    def mock_read_csv(path):

        calls['read_csv']+=1
        return pd.DataFrame({
            "feature1":[1,2,3],
            "price":[2,5,7]
        })

    monkeypatch.setattr('src.model.model_training.mlflow.set_experiment', mock_set_experiment)
    monkeypatch.setattr('src.model.model_training.train_model', mock_train_model)
    monkeypatch.setattr('src.model.model_training.pd.read_csv', mock_read_csv)
    monkeypatch.setattr('src.model.model_training.mlflow.set_tracking_uri', mock_set_tracking_uri)
    
    main()

    assert calls["mock_set_tracking"]
    assert calls["read_csv"]==2
    assert calls["set_experiment"]
    assert calls["train_model"]

