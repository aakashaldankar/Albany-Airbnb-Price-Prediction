from src.data.data_preprocessing import pre_preprocessing, main
from confest import sample_dataframe
import pandas as pd


def test_pre_processing(sample_dataframe):

    df=pre_preprocessing(sample_dataframe)

    assert df['host_since'].isnull().sum()==0
    assert df['host_location'].isnull().sum()==0
    assert df['host_response_time'].isnull().sum()==0
    assert df['host_response_rate'].isnull().sum()==0
    assert df['host_acceptance_rate'].isnull().sum()==0
    assert df['host_total_listings_count'].isnull().sum()==0
    assert df['host_verifications'].isnull().sum()==0
    assert df['host_has_profile_pic'].isnull().sum()==0
    assert df['host_identity_verified'].isnull().sum()==0
    assert df['bathrooms_text'].isnull().sum()==0
    assert df['beds'].isnull().sum()==0
    assert df['minimum_minimum_nights'].isnull().sum()==0
    assert df['maximum_minimum_nights'].isnull().sum()==0
    assert df['minimum_maximum_nights'].isnull().sum()==0
    assert df['maximum_maximum_nights'].isnull().sum()==0
    assert df['first_review'].isnull().sum()==0

    assert not {'host_name', 'description'}.issubset(df.columns)



def test_main(monkeypatch, tmp_path):

    calls={
        'pre_processing': False
    }

    mock_train_path=tmp_path/'train.csv'
    mock_test_path=tmp_path/'test.csv'

    df=pd.DataFrame({'price': [1,2,3]})
    df.to_csv(mock_train_path)
    df.to_csv(mock_test_path)

    def mock_pre_processing(df):

        calls['pre_processing']=True
        return df
    
    monkeypatch.setattr('src.data.data_preprocessing.train_data_file_path',mock_train_path)
    monkeypatch.setattr('src.data.data_preprocessing.test_data_file_path',mock_test_path)
    monkeypatch.setattr('src.data.data_preprocessing.processed_path',tmp_path)
    monkeypatch.setattr('src.data.data_preprocessing.processed_path',tmp_path)
    monkeypatch.setattr('src.data.data_preprocessing.pre_preprocessing',mock_pre_processing)

    main()

    saved_path1=(tmp_path/'pre_processed_train.csv')
    saved_path2=(tmp_path/'pre_processed_test.csv')

    assert calls['pre_processing']
    assert saved_path1.exists
    assert saved_path2.exists
    

    






