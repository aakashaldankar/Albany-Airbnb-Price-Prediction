from src.data.data_ingestion import load_params

def test_load_params():

    params=load_params('params.yaml')

    assert isinstance(params, dict)

    assert 'data_ingestion' in params
    assert 'test_size' in params['data_ingestion']
    assert isinstance(params['data_ingestion']['test_size'], float)

    assert 'feature_engineering' in params
    assert 'max_features' in params['feature_engineering']
    assert isinstance(params['feature_engineering']['max_features'], int)

    assert 'model_training' in params
    assert 'hyper_parameters' in params['model_training']
    assert 'n_estimators' in params['model_training']['hyper_parameters']
    assert 'max_depth' in params['model_training']['hyper_parameters']
    assert 'learning_rate' in params['model_training']['hyper_parameters']
    assert 'subsample' in params['model_training']['hyper_parameters']
    assert isinstance(params['model_training']['hyper_parameters']['n_estimators'], int)
    assert isinstance(params['model_training']['hyper_parameters']['max_depth'], int)
    assert isinstance(params['model_training']['hyper_parameters']['learning_rate'], float)
    assert isinstance(params['model_training']['hyper_parameters']['subsample'], float)

# def test_pre_processing(sample_df):




