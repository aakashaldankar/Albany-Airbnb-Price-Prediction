import pandas as pd
import os
from src.logger import get_logger
import re
import ast
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

script_name=os.path.basename(__file__)
logger=get_logger(script_name)

train_data_filename='train_data.csv'
test_data_filename='test_data.csv'

root_dir=os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
extracted_data_path=os.path.join(root_dir,'central_data','raw_data')
print(extracted_data_path)

processed_path=os.path.join(root_dir,'central_data','pre_processed')
os.makedirs(processed_path, exist_ok=True)

train_data_file_path=os.path.join(extracted_data_path, train_data_filename)
test_data_file_path=os.path.join(extracted_data_path, test_data_filename)

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
    except:
        return 0
    

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
        value=int(sum(value_couns.values[:10])/10)
        df['host_total_listings_count']=df['host_total_listings_count'].fillna(value) # here we impute the missing value with the average of top 10 value occurences. 
        
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

        row_indexes=df.index[df['first_review'].isnull()].tolist()
        df.drop(index=row_indexes, inplace=True)
        
        indexes=df['host_verifications'].value_counts().index
        hverification_encoder={}
        j=0 
        for i in indexes:
            hverification_encoder.update({i:j})
            j+=1
        
        df['host_verifications']=df['host_verifications'].apply(lambda x: hverification_encoder.get(x))

        neighbour_cleansed=df.groupby('neighbourhood_cleansed')['price'].mean()
        df['neighbourhood_cleansed_encoded']=df['neighbourhood_cleansed'].map(neighbour_cleansed)
        
        df.drop(columns=['neighbourhood_cleansed'], inplace=True)

        property_type_mapping=df.groupby('property_type')['price'].mean()
        df['property_type_encoded']=df['property_type'].map(property_type_mapping)
        df.drop(columns=['property_type'], inplace=True)

        df['room_type']=df['room_type'].replace({'Hotel room': 'Other', 'Shared room': 'Other'})
        df=pd.get_dummies(df, columns=['room_type'], drop_first=True, dtype=int)

        df['bathroom_count']=df['bathrooms_text'].apply(extract_bathroom_number)
        df.drop(columns=['bathrooms_text'], inplace=True)

        df['amenity_count']=df['amenities'].apply(lambda x: count_amenities(x))
        df.drop(columns=['amenities'], inplace=True)

        df.drop(columns=['host_name'], inplace=True)

        df.drop(columns=['description'], inplace=True)

        logger.info('null values pre-processed successfully')

        return df

    except Exception as e:
        logger.error('Unexpected error, %s', e)

def main():

    try:

        train_df=pd.read_csv(train_data_file_path)
        test_df=pd.read_csv(test_data_file_path)

        train_pre_processed=pre_preprocessing(train_df)
        test_pre_processed=pre_preprocessing(test_df)

        for i in ['name', 'host_location']: # Here we perform tfid on these columns

            tfidf=TfidfVectorizer(stop_words='english', max_features=20)

            x_train=tfidf.fit_transform(train_pre_processed[i])
            x_test=tfidf.transform(test_pre_processed[i])

            Train_df=pd.DataFrame(x_train.toarray(), columns=tfidf.get_feature_names_out())
            Test_df=pd.DataFrame(x_test.toarray(), columns=tfidf.get_feature_names_out())

            train_pre_processed=train_pre_processed.reset_index(drop=True)
            Train_df=Train_df.reset_index(drop=True)

            test_pre_processed=test_pre_processed.reset_index(drop=True)
            Test_df=Test_df.reset_index(drop=True)

            train_pre_processed=pd.concat([train_pre_processed, Train_df], axis=1)
            test_pre_processed=pd.concat([test_pre_processed, Test_df], axis=1)

            train_pre_processed.drop(columns=[i], inplace=True)
            test_pre_processed.drop(columns=[i], inplace=True)
        
        train_pre_processed.to_csv(os.path.join(processed_path, 'pre_processed_train.csv'))
        test_pre_processed.to_csv(os.path.join(processed_path, 'pre_processed_test.csv'))  

        logger.info('train and test data pre-processed successfully')      

    except Exception as e:
        logger.error('Unexpected Error, %e', e)
        raise 

if __name__=='__main__':
    main()
