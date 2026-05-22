from src.model.model_evaluation import register_model, is_eligible, get_prod_metrics, beats_production, main

def test_register_model(monkeypatch):

    class MockRun:

        class info:
            experiment_id=10
        
        class data:
            metrics={'mean_absolute_error': 0.54, 
                     'mean_squared_error': 0.45,
                     'root_mean_squared_error': 0.67}
        
    class MockSeachedModels:

        model_uri='http:aakashaldankar.com'

    class MockModelVersion:

        version=1

    def mock_get_run(run_id):
        return MockRun
    
    def mock_search_logged_models(experiment_ids, filter_string):
        return [MockSeachedModels]
    
    def mock_register_model(model_uri, model_name):
        return MockModelVersion
    
    monkeypatch.setattr('src.model.model_evaluation.client.get_run', mock_get_run)
    monkeypatch.setattr('src.model.model_evaluation.client.search_logged_models', mock_search_logged_models)
    monkeypatch.setattr('src.model.model_evaluation.mlflow.register_model', mock_register_model)

    run_id=1
    model_name='test_model'

    metrics, version=register_model(run_id, model_name)

    assert metrics=={'mean_absolute_error': 0.54, 'mean_squared_error': 0.45,'root_mean_squared_error': 0.67}
    assert version==1


    

    


