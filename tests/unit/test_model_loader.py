from app.model_loader import load_model, load_encoders, main
import mlflow.pyfunc

def test_load_model(monkeypatch):

    class LoadModel:
        model=10
    
    def mock_load_model(uri):

        assert uri=="models:/testmodel@champion"
        return LoadModel()
    
    monkeypatch.setattr("app.model_loader.mlflow.pyfunc.load_model",mock_load_model)

    result=load_model("testmodel", "champion")

    assert isinstance(result, LoadModel)

def test_load_encoders(monkeypatch, tmp_path):

    encoders={"target_encoders": 1234}
    encoders_path=tmp_path

    def mock_load(encoders_path):
        return encoders
    
    monkeypatch.setattr("app.model_loader.joblib.load",mock_load)

    result=load_encoders()

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

    monkeypatch.setattr("app.model_loader.load_model", mock_load_model)
    monkeypatch.setattr("app.model_loader.load_encoders", mock_load_encoders)

    main()

    assert calls["loader_encoders"]
    assert calls["load_model"]