from src.model.model_evaluation import register_model, is_eligible, get_prod_metrics, beats_production, main
import json

def test_register_model(monkeypatch, tmp_path):

    class MockRun:

        class info:
            experiment_id=10
        
        class data:
            metrics={'mean_absolute_error': 0.54, 
                     'mean_squared_error': 0.45,
                     'root_mean_squared_error': 0.67}
        
    class MockSeachedModels:
        model_uri='http:aakashaldankar.com'

    class MockClient:

        def get_run(self, run_id):
            return MockRun
        
        def search_logged_models(self, experiment_ids, filter_string):
            return [MockSeachedModels]

    class MockModelVersion:
        version=1

    def mock_register_model(model_uri, model_name):
        return MockModelVersion
    
    mock_run_id_path=tmp_path/'run_info.json'

    with open(mock_run_id_path, 'w') as f:
        json.dump({'run_id':1},f)

    monkeypatch.setattr('src.model.model_evaluation.mlflow.register_model', mock_register_model)
    monkeypatch.setattr('src.model.model_evaluation.run_id_path', mock_run_id_path)

    run_id=1
    model_name='test_model'
    client=MockClient()


    metrics, version=register_model(run_id, model_name, client)

    assert metrics=={'mean_absolute_error': 0.54, 'mean_squared_error': 0.45,'root_mean_squared_error': 0.67}
    assert version==1

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
    
    # monkeypatch.setattr('src.model.model_evaluation.client.get_model_version_by_alias',mock_get_model_version_by_alias)
    # monkeypatch.setattr('src.model.model_evaluation.client.get_run',mock_get_run)

    model_name='test_model'
    client=MockClient()

    result=get_prod_metrics(model_name, client)

    assert result=={'mean_absolute_error': 0.54, 'mean_squared_error': 0.45,'root_mean_squared_error': 0.67}

def test_beats_production():

    new_metrics={'mean_absolute_error': 1, 'mean_squared_error': 1,'root_mean_squared_error': 1}
    prod_metrics={'mean_absolute_error': 2, 'mean_squared_error': 2,'root_mean_squared_error': 2}

    result=beats_production(new_metrics, prod_metrics)

    assert result

def test_main(monkeypatch):

    calls={
        "register_model": False,
        "is_eligible": False,
        "get_prod_metrics": False,
        "beats_production": False,
        "get_model_version_by_alias": False,
        "set_registered_model_alias": 0
    }

    def mock_register_model(run_id, model_name, client):

        calls["register_model"]=True
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


    monkeypatch.setattr("src.model.model_evaluation.register_model",mock_register_model)
    monkeypatch.setattr("src.model.model_evaluation.is_eligible",mock_is_eligible)
    monkeypatch.setattr("src.model.model_evaluation.get_prod_metrics",mock_get_prod_metrics)
    monkeypatch.setattr("src.model.model_evaluation.beats_production",mock_beats_production)
    monkeypatch.setattr("src.model.model_evaluation.MlflowClient",MockMlflowClient)
    monkeypatch.setattr("src.model.model_evaluation.MlflowClient",MockMlflowClient)

    main()

    assert calls['beats_production']
    assert calls['get_model_version_by_alias']
    assert calls['get_prod_metrics']
    assert calls['is_eligible']
    assert calls['register_model']
    assert calls['set_registered_model_alias']==2
    