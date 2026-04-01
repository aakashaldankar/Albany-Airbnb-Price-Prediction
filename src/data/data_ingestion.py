from src.logger import get_logger 
import pandas as pd
import os

logger=get_logger("src.data_ingestion")
extracted_data_path='data'

def load_data(url: str):
    try:
        df=pd.read_csv(url)
        logger.info("Loaded the dataset from, %s", url)
        return df
        
    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise

def save_data(df: pd.DataFrame, folder: str):

    try:
        path=os.path.join(extracted_data_path,folder, 'extracted_data.csv')
        os.makedirs(os.path.join(extracted_data_path,folder), exist_ok=True)
        df.to_csv(path)
        logger.info("extracted data saved in, %s", path)

    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise

def main():

    try: 
        df=load_data('https://raw.githubusercontent.com/aakashaldankar/Albany-Airbnb-Listings-Data/refs/heads/main/listings.csv')
        save_data(df, folder='raw_data')

    except Exception as e:
        logger.error('Unexpected error, %e', e)
        raise

if __name__=='__main__':
    main()



        







        
