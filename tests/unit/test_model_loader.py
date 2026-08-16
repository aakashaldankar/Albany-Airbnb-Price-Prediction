from app.model_loader import load_best_model, load_encoders, main, load_params
import app.model_loader as model_loader
import mlflow.pyfunc
import os
import yaml

MODEL_NAME = os.getenv("MODEL_NAME", "albany price predictor")
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "champion")

def test_load_best_model(monkeypatch):

    class LoadModel:
        model=10
    
    def mock_load_model(uri):

        assert uri=="models:/testmodel@champion"
        return LoadModel()
    
    monkeypatch.setattr("app.model_loader.mlflow.pyfunc.load_model",mock_load_model)

    result=load_best_model("testmodel", "champion")

    assert isinstance(result, LoadModel)

def test_load_encoders(monkeypatch, tmp_path):

    class ModelVersion:

        def __init__(self):
            self.run_id=1

    class MlFlowClient:

        def get_model_version_by_alias(self, model_name, alias):
            return ModelVersion()
    
    def mock_download_artifacts(artifact_uri="artifacts"):
        return {"target_encoders": 1234}

    def mock_load(encoder_file):
        return encoder_file
    
    monkeypatch.setattr("app.model_loader.joblib.load",mock_load)
    monkeypatch.setattr("app.model_loader.MlflowClient", MlFlowClient)
    monkeypatch.setattr("app.model_loader.download_artifacts", mock_download_artifacts)

    result=load_encoders(MODEL_NAME, MODEL_ALIAS)

    assert result=={"target_encoders": 1234}

def test_load_params(tmp_path):

    params={"1": 1}

    params_path=tmp_path/'params.yaml'

    with open(params_path,'w') as f:
        yaml.dump(params, f)

    result=load_params(params_path)

    assert result==params


def test_main(monkeypatch):

    calls={
        "load_model": False,
        "loader_encoders": False,
        "load_params": False
    }

    def mock_load_model(model_name, alias):
        calls["load_model"]=True

    def mock_load_encoders(model_name, alias):
        calls["loader_encoders"]=True
    
    def mock_load_params(params_path: str):
        calls['load_params']=True
        return {"model_name": "zer0"}

    monkeypatch.setattr("app.model_loader.load_best_model", mock_load_model)
    monkeypatch.setattr("app.model_loader.load_encoders", mock_load_encoders)
    monkeypatch.setattr('app.model_loader.load_params', mock_load_params)

    main()

    assert calls["loader_encoders"]
    assert calls["load_model"]
    assert calls['load_params']


def test_load_model_populates_cache(monkeypatch):

    monkeypatch.setattr(model_loader, "_model", None)
    monkeypatch.setattr(model_loader, "_encoders", None)
    monkeypatch.setattr(model_loader, "_model_version", None)

    class ModelVersion:
        version = "3"

    class MlFlowClient:
        def get_model_version_by_alias(self, model_name, alias):
            return ModelVersion()

    calls = {"load_best_model": 0, "load_encoders": 0}

    def mock_load_best_model(model_name, alias):
        calls["load_best_model"] += 1
        return "model-obj"

    def mock_load_encoders(model_name, alias):
        calls["load_encoders"] += 1
        return "encoders-obj"

    monkeypatch.setattr(model_loader, "load_best_model", mock_load_best_model)
    monkeypatch.setattr(model_loader, "load_encoders", mock_load_encoders)
    monkeypatch.setattr(model_loader, "MlflowClient", MlFlowClient)

    model, encoders = model_loader.load_model()

    assert model == "model-obj"
    assert encoders == "encoders-obj"
    assert model_loader.get_model_version() == "3"
    assert calls["load_best_model"] == 1
    assert calls["load_encoders"] == 1


def test_get_model_and_get_encoders_are_cached(monkeypatch):

    monkeypatch.setattr(model_loader, "_model", None)
    monkeypatch.setattr(model_loader, "_encoders", None)
    monkeypatch.setattr(model_loader, "_model_version", None)

    calls = {"load_model": 0}

    def mock_load_model():
        calls["load_model"] += 1
        model_loader._model = "cached-model"
        model_loader._encoders = "cached-encoders"

    monkeypatch.setattr(model_loader, "load_model", mock_load_model)

    result_model = model_loader.get_model()
    result_encoders = model_loader.get_encoders()

    assert result_model == "cached-model"
    assert result_encoders == "cached-encoders"
    assert calls["load_model"] == 1