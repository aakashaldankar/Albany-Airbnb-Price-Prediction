from src.logger import get_logger 
import pandas as pd
import os
from sklearn.model_selection import train_test_split

script_name = os.path.basename(__file__)
logger=get_logger(script_name)
data_path='central_data'

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
        df=load_data('https://raw.githubusercontent.com/aakashaldankar/Albany-Airbnb-Listings-Data/refs/heads/main/listings.csv')
        pre_processed_df=pre_processing(df)
        train_data, test_data = train_test_split(pre_processed_df, test_size=0.3, random_state=10, shuffle=True)

        save_data(train_data, folder='raw_data', file_name='train_data')
        save_data(test_data, folder='raw_data', file_name='test_data')

    except Exception as e:
        logger.error('Unexpected error, %e', e)
        raise

if __name__=='__main__':
    main()



        







        
