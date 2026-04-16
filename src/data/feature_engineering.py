import pandas as pd
import os
from datetime import datetime
from src.logger import get_logger

script_name=os.path.basename(__file__)
logger=get_logger(script_name)

train_df='pre_processed_train.csv'
test_df='pre_processed_test.csv'

root_dir=os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
data_path=os.path.join(root_dir, 'central_data','pre_processed')



def feature_engineering(df: pd.DataFrame):

    try: 

        df['host_response_rate']=df['host_response_rate'].apply(lambda x: int(x[:-1]))
        df['host_acceptance_rate']=df['host_acceptance_rate'].apply(lambda x: int(x[:-1]))
        df['host_is_superhost']=df['host_is_superhost'].apply(lambda x: 1 if x=='t' else 0)

        df['host_has_profile_pic']=df['host_has_profile_pic'].apply(lambda x: 1 if x=='t' else 0)
        df['host_identity_verified']=df['host_identity_verified'].apply(lambda x: 1 if x=='t' else 0)
        df['price']=df['price'].apply(lambda x: float(x[1:].replace(',', '')))

        df['has_availability']=df['has_availability'].apply(lambda x: 1 if x=='t' else 0)
        df['first_review']=df['first_review'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').year)
        df['last_review']=df['last_review'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').year)

        df['instant_bookable']=df['instant_bookable'].apply(lambda x: 1 if x=='t' else 0)
        
        df['host_response_time']=df['host_response_time'].replace({'within an hour': 5, 'within a few hours': 4, 'within a day': 3, 'a few days or more': 2, 'not specified': 1})

        logger.info('feature transformation successfully performed')

        return df

    except Exception as e:

        logger.error('Unexpected error, %e', e)
        raise



def label_encoding(df: pd.DataFrame, column_name: str):
    """"
    Here we perform label encoding on the column name provided
    """

    try: 
        encoder={i:v for v,i in enumerate(df[column_name].value_counts().index)}
        df[column_name]=df[column_name].map(encoder)

        logger.info(f'performed label encoding on column {column_name} successfully')
        
        return df

    except Exception as e:
        logger.error('unexpected error occured, %s', e)
        raise



def target_encoding(df: pd.DataFrame, column_name: str, target_column: str):
    """
    Here we perform target encoding on the column name specified wrt to the target column specified. 
    Specifically this is called mean encoding, a subset of target encoding.
    """
    
    try:

        target_encoder=df.groupby(column_name)[target_column].mean()
        df[column_name]=df[column_name].map(target_encoder)

        logger.info(f'target encoding performed on column {column_name} successfully')
        
        return df
    
    except Exception as e:

        logger.error('unexpected error occured, %s', e)
        raise



def one_hot_encoding(df: pd.DataFrame, column_name: str):
    """
    Here we perform one-hot encoding on the specified column name. 
    To avoid the dummy variable trap, a situation where one column is 
    perfectly predictable from the others (multicollinearity). 
    This can destabilize linear models like Linear Regression or Logistic Regression. 
    So dropping one column carries the same information with less redundancy.
    """
    
    try: 

        df=pd.get_dummies(df, columns=[column_name], drop_first=True, dtype=int)
        
        logger.info(f'one-hot encoding performed on column {column_name} successfully')

        return df
    
    except Exception as e:

        logger.error('unexpected error occurred, %s', e)
        raise






    
