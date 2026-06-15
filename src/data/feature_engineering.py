import pandas as pd
import os
from datetime import datetime
from src.logger import get_logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
import re
import ast
import joblib
import numpy as np
import yaml

script_name=os.path.basename(__file__)
logger=get_logger(script_name)

train_df='pre_processed_train.csv'
test_df='pre_processed_test.csv'

root_dir=os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
data_path=os.path.join(root_dir, 'central_data','pre_processed')

encoder_path=os.path.join(root_dir, 'artifacts', 'feature_encoders')
os.makedirs(encoder_path, exist_ok=True)

save_data_path=os.path.join(root_dir, 'central_data', 'feature_engineering')
os.makedirs(save_data_path, exist_ok=True)

def load_params(params_path: str):

    try: 

        with open(params_path, 'r') as file:
            params=yaml.safe_load(file)

        logger.info('params loaded successfully')

        return params
    
    except Exception as e:
        logger.error('unexpected error occurred, %s', e)
        raise

def extract_bathroom_number(text):
    if pd.isna(text):
        return None
    
    # Extract numbers (including decimals)
    numbers = re.findall(r'\d+\.?\d*', str(text))
    
    if numbers:
        return float(numbers[0])
    elif 'half' in str(text).lower():
        return 0.5
    else:
        return 0
    
def count_amenities(amenity_string):
    if pd.isna(amenity_string):
        return 0
    try:
        amenity_list = ast.literal_eval(amenity_string)
        return len(amenity_list)
    except Exception:
        return 0

def feature_transform(df: pd.DataFrame):

    try: 

        df['host_response_rate']=df['host_response_rate'].apply(lambda x: int(x[:-1]))
        df['host_acceptance_rate']=df['host_acceptance_rate'].apply(lambda x: int(x[:-1]))
        df['host_is_superhost']=df['host_is_superhost'].apply(lambda x: 1 if x=='t' else 0)

        df['host_has_profile_pic']=df['host_has_profile_pic'].apply(lambda x: 1 if x=='t' else 0)
        df['host_identity_verified']=df['host_identity_verified'].apply(lambda x: 1 if x=='t' else 0)
        df['price']=df['price'].apply(lambda x: float(x[1:].replace(',', '')))
        df['price']=np.log1p(df['price']) # log(1 + price)
        # Remember to inverse-transform predictions: np.expm1(y_pred)

        df['has_availability']=df['has_availability'].apply(lambda x: 1 if x=='t' else 0)
        df['first_review']=df['first_review'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').year)
        df['last_review']=df['last_review'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').year)
        df['host_since']=df['host_since'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').year) 

        df['instant_bookable']=df['instant_bookable'].apply(lambda x: 1 if x=='t' else 0)
        
        df['host_response_time']=df['host_response_time'].map({'within an hour': 5, 'within a few hours': 4, 'within a day': 3, 'a few days or more': 2, 'not specified': 1})

        df['bathrooms_text']=df['bathrooms_text'].apply(extract_bathroom_number)

        df['amenities']=df['amenities'].apply(lambda x: count_amenities(x))
        
        logger.info('feature transformation successfully performed')

        return df

    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise


def label_encoding(train_df: pd.DataFrame, test_df: pd.DataFrame, column_name: str):
    """"
    Here we perform label encoding on the column name provided
    """

    try: 
        encoder={i:v for v,i in enumerate(train_df[column_name].value_counts().index)}
        train_df[column_name]=train_df[column_name].map(encoder)
        test_df[column_name]=test_df[column_name].map(encoder)

        logger.info(f'performed label encoding on column {column_name} successfully')
        
        return train_df, test_df, encoder

    except Exception as e:
        logger.error('unexpected error occured, %s', e)
        raise


def target_encoding(train_df: pd.DataFrame, test_df: pd.DataFrame, column_name: str, target_column: str):
    """
    Here we perform target encoding on the column name specified wrt to the target column specified. 
    Specifically this is called mean encoding, a subset of target encoding.
    """
    
    try:

        target_encoder=train_df.groupby(column_name)[target_column].mean()
        train_df[column_name]=train_df[column_name].map(target_encoder)
        test_df[column_name]=test_df[column_name].map(target_encoder)

        logger.info(f'target encoding performed on column {column_name} successfully')
        
        return train_df, test_df, target_encoder
    
    except Exception as e:

        logger.error('unexpected error occured, %s', e)
        raise


def one_hot_encoding(train_df: pd.DataFrame, test_df: pd.DataFrame, column_name: str):
    """
    Performs one-hot encoding using sklearn's OneHotEncoder with proper 
    fit/transform separation to avoid data leakage.
    - Fits only on training data
    - Applies to both train and test
    - drop='first' to avoid dummy variable trap
    - handle_unknown='ignore' to handle unseen categories in real-life data
    """
    
    try:
        ohe = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore', dtype=int)

        # Fit only on train, apply to both
        train_encoded = ohe.fit_transform(train_df[[column_name]])
        test_encoded = ohe.transform(test_df[[column_name]])

        # Get feature names and convert to dataframe
        feature_names = ohe.get_feature_names_out([column_name])
        
        train_df[feature_names] = train_encoded
        test_df[feature_names] = test_encoded

        # Drop original column
        train_df.drop(columns=[column_name], inplace=True)
        test_df.drop(columns=[column_name], inplace=True)

        logger.info(f'one-hot encoding performed on column {column_name} successfully')

        return train_df, test_df, ohe  # return ohe to save later

    except Exception as e:
        logger.error('unexpected error occurred, %s', e)
        raise


def tfidf_nlp(train_df: pd.DataFrame, test_df: pd.DataFrame, column_name: str, max_features: int):

    try: 

        tfidf=TfidfVectorizer(stop_words='english', max_features=max_features)

        x_train=tfidf.fit_transform(train_df[column_name])
        x_test=tfidf.transform(test_df[column_name])

        # print(tfidf.get_feature_names_out())

        feature_names = [f"{column_name}_{feature}" for feature in tfidf.get_feature_names_out()]

        Train_df=pd.DataFrame(x_train.toarray(), columns=feature_names)
        Test_df=pd.DataFrame(x_test.toarray(), columns=feature_names)

        train_df=train_df.reset_index(drop=True)
        test_df=test_df.reset_index(drop=True)

        Train_df=Train_df.reset_index(drop=True)
        Test_df=Test_df.reset_index(drop=True)

        train_df=pd.concat([train_df, Train_df], axis=1)
        test_df=pd.concat([test_df, Test_df], axis=1)

        train_df.drop(columns=[column_name], inplace=True)
        test_df.drop(columns=[column_name], inplace=True)

        logger.info(f'performed tfidf on column {column_name} successfully')

        return train_df, test_df, tfidf
    
    except Exception as e:

        logger.error('unexpected error occured, %s', e)
        raise


def main():
        
    try: 

        artifacts={}

        params=load_params('params.yaml')
        max_features=params['feature_engineering']['max_features']

        train_df=pd.read_csv(os.path.join(data_path, 'pre_processed_train.csv'))
        test_df=pd.read_csv(os.path.join(data_path, 'pre_processed_test.csv'))

        train_df=feature_transform(train_df)
        test_df=feature_transform(test_df)

        train_df, test_df, host_verification_label_encoder = label_encoding(train_df=train_df, test_df=test_df, column_name='host_verifications')
        artifacts.update({'host_verification_label_encoder': host_verification_label_encoder})

        train_df, test_df, neighbourhood_cleansed_target_encoder = target_encoding(train_df=train_df, test_df=test_df, column_name='neighbourhood_cleansed', target_column='price')
        artifacts.update({'neighbourhood_cleansed_target_encoder': neighbourhood_cleansed_target_encoder})

        train_df, test_df, property_type_target_encoder = target_encoding(train_df=train_df, test_df=test_df, column_name='property_type', target_column='price')
        artifacts.update({'property_type_target_encoder': property_type_target_encoder})

        train_df['room_type']=train_df['room_type'].apply(lambda x: x if x in ['Entire home/apt', 'Private room'] else 'Other')
        test_df['room_type']=test_df['room_type'].apply(lambda x: x if x in ['Entire home/apt', 'Private room'] else 'Other')

        train_df, test_df, room_type_ohe = one_hot_encoding(train_df=train_df, test_df=test_df, column_name='room_type')
        artifacts.update({'room_type_ohe': room_type_ohe})

        train_df, test_df, name_tfidf_encoder = tfidf_nlp(train_df=train_df, test_df=test_df, column_name='name', max_features=max_features)
        artifacts.update({'name_tfidf_encoder': name_tfidf_encoder})

        train_df, test_df, host_location_tfidf_encoder = tfidf_nlp(train_df=train_df, test_df=test_df, column_name='host_location', max_features=max_features)
        artifacts.update({'host_location_tfidf_encoder': host_location_tfidf_encoder})

        joblib.dump(artifacts, os.path.join(encoder_path, 'feature_engineering_encoders.pkl'))
        logger.info(f'saved the artifacts of feature encoders to {os.path.join(encoder_path, 'feature_engineering_encoders.pkl')}')

        train_df.to_csv(os.path.join(save_data_path, 'final_train_data.csv'), index=False)
        test_df.to_csv(os.path.join(save_data_path, 'final_test_data.csv'), index=False)
        
        logger.info('performed feature engineering successfully')

    except Exception as e:

        logger.error('unexpected error occured, %s', e)
        raise

if __name__=='__main__':
    main()













    