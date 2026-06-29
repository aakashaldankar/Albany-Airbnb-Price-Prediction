from src.model.model_evaluation import get_latest_trained_metrics, is_eligible, get_prod_metrics, beats_production, main
import json

# def test_register_model(monkeypatch):

#     class MockRun:

#         class info:
#             experiment_id=10
        
#         class data:
#             metrics={'mean_absolute_error': 0.54, 
#                      'mean_squared_error': 0.45,
#                      'root_mean_squared_error': 0.67}
        
#     class MockSeachedModels:
#         model_uri='http:aakashaldankar.com'

#     class MockClient:

#         def get_run(self, run_id):
#             return MockRun
        
#         def search_logged_models(self, experiment_ids, filter_string):
#             return [MockSeachedModels]

#     class MockModelVersion:
#         version=1

#     def mock_register_model(model_uri, model_name):
#         return MockModelVersion

#     monkeypatch.setattr('src.model.model_evaluation.mlflow.register_model', mock_register_model)

#     run_id=1
#     model_name='test_model'
#     client=MockClient()

#     metrics, version=register_model(run_id, model_name, client)

#     assert metrics=={'mean_absolute_error': 0.54, 'mean_squared_error': 0.45,'root_mean_squared_error': 0.67}
#     assert version==1

def test_get_latest_trained_metrics():

    class LatestTrainedVersion:

        def __init__(self):
            self.run_id=1
            self.version=1

    class Metrics:

        def __init__(self):
            self.metrics=1
        
    class LatestTrainedRun:

        def __init__(self):
            self.data=Metrics()

    class Client:

        def get_model_version_by_alias(self, model_name: str, alias: str):
            return LatestTrainedVersion()
        
        def get_run(self, run_id: int):
            return LatestTrainedRun()
        
    model_name='model_1'
    client=Client()
        
    metrics, version = get_latest_trained_metrics(model_name, client)

    assert metrics == 1
    assert version == 1

def test_is_eligible():

    metrics={'mean_absolute_error': 1, 'mean_squared_error': 1,'root_mean_squared_error': 1}
    threshold_metrics={'mean_absolute_error': 2, 'mean_squared_error': 2,'root_mean_squared_error': 2}

    assert is_eligible(metrics, threshold_metrics)

def test_get_prod_metrics(monkeypatch):

    class ProdVersion:
        run_id=10

    class GetRun:

        class data:
            metrics={'mean_absolute_error': 0.54, 'mean_squared_error': 0.45,'root_mean_squared_error': 0.67}

    class MockClient:

        def get_model_version_by_alias(self, model_name, name):
            return ProdVersion
        
        def get_run(self, prod_run_id):
            return GetRun

    model_name='test_model'
    client=MockClient()

    result=get_prod_metrics(model_name, client)

    assert result=={'mean_absolute_error': 0.54, 'mean_squared_error': 0.45,'root_mean_squared_error': 0.67}

def test_beats_production():

    new_metrics={'mean_absolute_error': 1, 'mean_squared_error': 1,'root_mean_squared_error': 1}
    prod_metrics={'mean_absolute_error': 2, 'mean_squared_error': 2,'root_mean_squared_error': 2}

    result=beats_production(new_metrics, prod_metrics)

    assert result

def test_main(monkeypatch, tmp_path):

    calls={
        "get_latest_trained_metrics": False,
        "is_eligible": False,
        "get_prod_metrics": False,
        "beats_production": False,
        "get_model_version_by_alias": False,
        "set_registered_model_alias": 0
    }

    def mock_get_latest_trained_metrics(model_name: str, client):

        calls['get_latest_trained_metrics']=True
        
        metrics={'mean_absolute_error': 1, 'mean_squared_error': 1,'root_mean_squared_error': 1}
        version=1

        return metrics, version

    def mock_is_eligible(metrics, threshold):

        calls["is_eligible"]=True

        return True
    
    def mock_get_prod_metrics(model_name, client):
        
        calls["get_prod_metrics"]=True
        metrics={'mean_absolute_error': 2, 'mean_squared_error': 2,'root_mean_squared_error': 2}

        return metrics
    
    def mock_beats_production(metrics, prod_metrics):

        calls["beats_production"]=True
        return True
    
    class GetModelVersion:

        version=1

    class MockMlflowClient:

        def get_model_version_by_alias(self, model_name, name):
            calls["get_model_version_by_alias"]=True
            return GetModelVersion
        
        def set_registered_model_alias(self, model_name, name, old_champ_version):
            calls["set_registered_model_alias"]+=1

    mock_root_dir=tmp_path

    params_file=tmp_path/'params.yaml'

    with open(params_file, 'w') as f:
        json.dump({'tracking_uri': "model_uri", 'model_name': "albany-price-predictor"}, f)

    monkeypatch.setattr("src.model.model_evaluation.get_latest_trained_metrics",mock_get_latest_trained_metrics)
    monkeypatch.setattr("src.model.model_evaluation.is_eligible",mock_is_eligible)
    monkeypatch.setattr("src.model.model_evaluation.get_prod_metrics",mock_get_prod_metrics)
    monkeypatch.setattr("src.model.model_evaluation.beats_production",mock_beats_production)
    monkeypatch.setattr("src.model.model_evaluation.MlflowClient",MockMlflowClient)
    monkeypatch.setattr("src.model.model_evaluation.MlflowClient",MockMlflowClient)
    monkeypatch.setattr("src.model.model_evaluation.root_dir",mock_root_dir)

    main()

    assert calls['beats_production']
    assert calls['get_model_version_by_alias']
    assert calls['get_prod_metrics']
    assert calls['is_eligible']
    assert calls['get_latest_trained_metrics']
    assert calls['set_registered_model_alias']==2
    