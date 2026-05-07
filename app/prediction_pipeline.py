from app.model_loader import load_model, load_encoders
import os
import pandas as pd

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

train_data_path=os.path.join(root_dir, 'central_data', 'raw_data','train_data.csv')

df=pd.read_csv(train_data_path)

print(df.info())


# def pre_process(data: dict):




