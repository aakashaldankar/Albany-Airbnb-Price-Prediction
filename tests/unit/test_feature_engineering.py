from src.data.feature_engineering import load_params, extract_bathroom_number, count_amenities, feature_transform, label_encoding, target_encoding, one_hot_encoding, tfidf_nlp, main
import numpy as np
import pandas as pd
import os

def test_load_params():

    result=load_params('params.yaml')

    assert 'feature_engineering' in result
    assert 'max_features' in result['feature_engineering']

def test_extract_bathroom_number():

    assert extract_bathroom_number("")==0
    assert extract_bathroom_number("1.5 bathrooms")==1.5
    assert extract_bathroom_number("half sized bathroom")==0.5

def test_count_amenities():

    assert count_amenities("['bathroom', 'table', 'wifi']")==3
    assert count_amenities("")==0

def test_feature_transform(sample_feature_df):

    df=feature_transform(sample_feature_df)

    assert df['host_response_rate'][0]==90
    assert df['host_acceptance_rate'][0]==80
    assert df['host_is_superhost'][0]==1
    assert df['host_has_profile_pic'][0]==1
    assert df['host_identity_verified'][0]==0
    assert np.isclose(df['price'][0], np.log1p(100.0))
    assert df['has_availability'][0]==1
    assert df['first_review'][0]==2020
    assert df['last_review'][0]==2024
    assert df['host_since'][0]==2015
    assert df['instant_bookable'][0]==0
    assert df['host_response_time'][0]==5
    assert df['bathrooms_text'][0]==1.5
    assert df['amenities'][0]==2

def test_label_encoding():

    train_df=pd.DataFrame({"colour": ["A","B","C"]})
    test_df=pd.DataFrame({"colour": ["B","C"]})

    train_df, test_df, encoder=label_encoding(train_df, test_df, "colour")

    assert train_df["colour"].dtype!=object
    assert isinstance(encoder, dict)

def test_target_encoding():

    train_df=pd.DataFrame({"colour": ["red","yellow","red","white","pink"], "price": [1.89, 4.89, 8.29, 9.12, 7.89]})
    test_df=pd.DataFrame({"colour": ["red","orange","white","pink"], "price": [6.89, 2.89, 7.12, 1.89]})

    train_df, test_df, _=target_encoding(train_df, test_df, "colour", "price")

    assert train_df['colour'][0].dtype!=object
    assert train_df['colour'][0]==5.09

def test_one_hot_encoding():

    train_df=pd.DataFrame({"shape": ["round", "square", "triangle", "circle"]})
    test_df=pd.DataFrame({"shape": ["trapezium", "square", "triangle", "circle"]})
    
    train_df, test_df, ohe=one_hot_encoding(train_df, test_df, "shape")

    assert "shape" not in train_df.columns


def test_tfidf_nlp():

    train_df=pd.DataFrame({"description":["this is a beautiful scene", "This is the bestest picture of the century","the light house smells haunted and exciting"]})
    test_df=pd.DataFrame({"description": ["This is not a car", "This is some tastiest chicken that I had so far", "This is the bestest project which I am working on"]})

    train_df, test_df, tfidf=tfidf_nlp(train_df, test_df, "description", 3)

    assert "description" not in train_df.columns

def test_main(tmp_path, monkeypatch):

    calls={
        "feature_transform": 0,
        "label_encoding": False,
        "target_encoding": 0,
        "one_hot_encoding": False,
        "tfidf_nlp": 0,
    }

    train_df=pd.DataFrame({"room_type": ['Entire home/apt',2,4]})
    test_df=pd.DataFrame({"room_type":[2,'Private room',6]})

    train_df.to_csv(os.path.join(tmp_path, 'pre_processed_train.csv'))
    test_df.to_csv(os.path.join(tmp_path, 'pre_processed_test.csv'))

    def mock_feature_transform(train_df):

        calls['feature_transform']+=1
        return train_df
    
    def mock_label_encoding(train_df, test_df, column_name="dummy"):

        calls['label_encoding']=True
        return train_df, test_df, column_name
    
    def mock_target_encoding(train_df, test_df, column_name="dummy", target_column="dummy1"):

        calls['target_encoding']+=1
        return train_df, test_df, column_name
    
    def mock_one_hot_encoding(train_df, test_df, column_name='dummy'):

        calls['one_hot_encoding']=True
        return train_df, test_df, column_name
    
    def mock_tfidf_nlp(train_df, test_df, column_name="dummy", max_features=10):

        calls['tfidf_nlp']+=1
        return train_df, test_df, column_name
    
    monkeypatch.setattr("src.data.feature_engineering.feature_transform",mock_feature_transform)
    monkeypatch.setattr("src.data.feature_engineering.label_encoding",mock_label_encoding)
    monkeypatch.setattr("src.data.feature_engineering.target_encoding",mock_target_encoding)
    monkeypatch.setattr("src.data.feature_engineering.one_hot_encoding",mock_one_hot_encoding)
    monkeypatch.setattr("src.data.feature_engineering.tfidf_nlp",mock_tfidf_nlp)
    monkeypatch.setattr("src.data.feature_engineering.encoder_path",tmp_path)
    monkeypatch.setattr("src.data.feature_engineering.save_data_path",tmp_path)
    monkeypatch.setattr("src.data.feature_engineering.data_path",tmp_path)

    main()

    saved_path1=(tmp_path/'pre_processed_train.csv')
    saved_path2=(tmp_path/'pre_processed_test.csv')
    saved_path3=(tmp_path/'feature_engineering_encoders.pkl')
    saved_path4=(tmp_path/'final_train_data.csv')
    saved_path5=(tmp_path/'final_test_data.csv')

    assert calls["feature_transform"]
    assert calls["label_encoding"]
    assert calls["one_hot_encoding"]
    assert calls["target_encoding"]==2
    assert calls["tfidf_nlp"]==2
    assert saved_path1.exists
    assert saved_path2.exists
    assert saved_path3.exists
    assert saved_path4.exists
    assert saved_path5.exists
