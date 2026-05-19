from src.logger import get_logger 
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import yaml

script_name = os.path.basename(__file__)
logger=get_logger(script_name)
data_path='central_data'



def load_params(params_path: str):
        
    try:

        with open(params_path, 'r') as file:
            params=yaml.safe_load(file)
        
        logger.info('loaded params successfully')
        return params

    except Exception as e:
        logger.error('unexpected error occured, %s', e)
        raise


def load_data(url: str):
    try:
        df=pd.read_csv(url)
        logger.info("Loaded the dataset from, %s", url)
        return df
        
    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise


def pre_processing(df: pd.DataFrame):

    try:
        row_indices=df.index[(df['price'].isnull())].tolist()
        df.drop(index=row_indices, inplace=True)
        logger.info(f'{len(row_indices)} rows having null/no prices are dropped successfully')
        df.drop(["id","listing_url",'scrape_id','last_scraped','source','picture_url','host_id',
                 'host_url','host_thumbnail_url','host_picture_url','host_listings_count',
                 'neighbourhood_group_cleansed','calendar_updated','calendar_last_scraped','license',
                 'neighborhood_overview','host_about','host_neighbourhood','neighbourhood','estimated_occupancy_l365d','estimated_revenue_l365d'], axis=1, inplace=True)
        logger.info(f'Dropped all the redundant columns')
        return df
    
    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise


def save_data(df: pd.DataFrame, folder: str, file_name: str):

    try:
        path=os.path.join(data_path,folder, f'{file_name}.csv')
        os.makedirs(os.path.join(data_path,folder), exist_ok=True)
        df.to_csv(path, index=False)
        logger.info(f"{file_name}.csv saved to, %s", path)

    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise



def main():
    
    try: 
        params=load_params('params.yaml')
        test_size=params['data_ingestion']['test_size']
        data_url=params['data_ingestion']['data_url']

        df=load_data(data_url)
        pre_processed_df=pre_processing(df)

        train_data, test_data = train_test_split(pre_processed_df, test_size=test_size, random_state=10, shuffle=True)

        save_data(train_data, folder='raw_data', file_name='train_data')
        save_data(test_data, folder='raw_data', file_name='test_data')

    except Exception as e:
        logger.error('Unexpected error, %e', e)
        raise

if __name__=='__main__':
    main()
    