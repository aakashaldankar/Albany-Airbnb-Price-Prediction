from src.logger import get_logger 
import pandas as pd

logger=get_logger("src.data_ingestion")

def load_data(url: str):
    try:
        df=pd.read_csv(url)
        return df
        logger.info("Loaded the dataset from, %s", url)
    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise

def drop_rows_null_price(df: pd.DataFrame):
    
    try:
        row_indices=df.index[(df['price'].isnull())].tolist()
        df.drop(index=row_indices, inplace=True)
        logger.info(f"Dropped {len(row_indices)} rows having price null")
        return df
    
    except Exception as e:
        logger.error('Unexpected error, %s', e)
        raise







        
