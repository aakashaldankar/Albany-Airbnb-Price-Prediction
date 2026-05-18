from src.data.data_ingestion import load_params, load_data, pre_processing, save_data
from confest import sample_dataframe
import pandas as pd

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

def test_load_data(tmp_path, sample_dataframe):

    sample_file_path=tmp_path/'sample.csv'
    sample_dataframe.to_csv(sample_file_path)

    df=load_data(sample_file_path)

    isinstance(df, pd.DataFrame)

def test_pre_processing(sample_dataframe):

    df=pre_processing(sample_dataframe)

    assert df['price'].isnull().sum()==0

    assert not {"id","listing_url",'scrape_id','last_scraped','source','picture_url','host_id',
                 'host_url','host_thumbnail_url','host_picture_url','host_listings_count',
                 'neighbourhood_group_cleansed','calendar_updated','calendar_last_scraped','license',
                 'neighborhood_overview','host_about','host_neighbourhood','neighbourhood','estimated_occupancy_l365d','estimated_revenue_l365d'}.issubset(df.columns)
    
def test_save_data(tmp_path, sample_dataframe, monkeypatch):

    monkeypatch.setattr('src.data.data_ingestion.data_path', str(tmp_path))
    save_data(sample_dataframe, folder="raw_data", file_name="train")
    saved_file = (tmp_path/"raw_data"/"train.csv")
    assert saved_file.exists()




    





