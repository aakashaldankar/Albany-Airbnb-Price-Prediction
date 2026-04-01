import pandas as pd
import os
from src.logger import get_logger

logger=get_logger(__file__)

train_data_filename='train_data.csv'
test_data_filename='test_data.csv'

root_dir=os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
extracted_data_path=os.path.join(root_dir,'central_data','raw_data')
print(extracted_data_path)

train_data_file_path=os.path.join(extracted_data_path, train_data_filename)
test_data_file_path=os.path.join(extracted_data_path, test_data_filename)

print(f'train data file path, {train_data_file_path}')
print(f'test data file path, {test_data_file_path}')

def pre_preprocessing(df: pd.DataFrame):

    try:
        df['description']=df['description'].fillna('No description available')
        df['host_name']=df['host_name'].fillna(df['host_name'].mode()[0])
        df['host_since']=df['host_since'].fillna(df['host_since'].mode()[0])
        df['host_location']=df['host_location'].fillna(df['host_location'].mode()[0])
        df['host_response_time']=df['host_response_time'].fillna('not specified')
        df['host_response_rate']=df['host_response_rate'].fillna(df['host_response_rate'].mode()[0])
        df['host_acceptance_rate']=df['host_acceptance_rate'].fillna(df['host_acceptance_rate'].mode()[0])
        df['host_is_superhost']=df['host_is_superhost'].fillna(df['host_is_superhost'].mode()[0])

        value_couns=df['host_total_listings_count'].value_counts()
        df['host_total_listings_count']=df['host_total_listings_count'].fillna(int(value_couns)) # here we impute the missing value with the average of top 15 value occurences. 
        
        df['host_verifications']=df['host_verifications'].fillna(df['host_verifications'].mode()[0])
        df['host_has_profile_pic']=df['host_has_profile_pic'].fillna(df['host_has_profile_pic'].mode()[0])
        df['host_identity_verified']=df['host_identity_verified'].fillna(df['host_identity_verified'].mode()[0])
        df['bathrooms_text']=df['bathrooms_text'].fillna(df['bathrooms_text'].mode()[0])
        df['bedrooms']=df['bedrooms'].fillna(df['bedrooms'].mode()[0])
        df['beds']=df['beds'].fillna(df['beds'].mode()[0])

        df['minimum_minimum_nights']=df['minimum_minimum_nights'].fillna(df['minimum_minimum_nights'].mode()[0])
        df['maximum_minimum_nights']=df['maximum_minimum_nights'].fillna(df['maximum_minimum_nights'].mode()[0])
        df['minimum_maximum_nights']=df['minimum_maximum_nights'].fillna(df['minimum_maximum_nights'].mode()[0])
        df['maximum_maximum_nights']=df['maximum_maximum_nights'].fillna(df['maximum_maximum_nights'].mode()[0])

        df['has_availability']=df['has_availability'].fillna(df['has_availability'].mode()[0])

        logger.info('null values pre-processed successfully')

    except Exception as e:
        logger.error('Unexpected error, %s', e)



