from src.model.model_training import train_model, load_params, main
# from confest import sample_train_data
from contextlib import contextmanager
import os

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
    




    



