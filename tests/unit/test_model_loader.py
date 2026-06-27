from app.model_loader import load_best_model, load_encoders, main
import mlflow.pyfunc
import os

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


def test_main(monkeypatch):

    calls={
        "load_model": False,
        "loader_encoders": False
    }

    def mock_load_model(model_name, alias):
        calls["load_model"]=True

    def mock_load_encoders():
        calls["loader_encoders"]=True

    monkeypatch.setattr("app.model_loader.load_best_model", mock_load_model)
    monkeypatch.setattr("app.model_loader.load_encoders", mock_load_encoders)

    main()

    assert calls["loader_encoders"]
    assert calls["load_model"]