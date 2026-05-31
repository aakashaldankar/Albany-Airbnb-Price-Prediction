from app.prediction_pipeline import prediction
import numpy as np
import pandas as pd
from pydantic import BaseModel

def test_predict(monkeypatch):

    calls={
        "pre_process": False,
        "predict": False
    }
        
    def mock_pre_process(data, encoders):
        calls['pre_process']=True
        return data
    
    class MockModel:

        def predict(self, data_df):

            assert isinstance(data_df, pd.DataFrame)
            assert data_df.shape[0]==1

            calls["predict"]=True
            return np.array([np.log1p(100)])
        
    class Request(BaseModel):

        feature1: int
        feature2: int
        feature3: float

    request=Request(feature1=1, feature2=2, feature3=3.8)
    encoders={"private_room": 1}

    monkeypatch.setattr("app.prediction_pipeline.pre_process", mock_pre_process)

    result=prediction(request=request, model=MockModel(), encoders=encoders)

    assert calls["predict"]
    assert calls["pre_process"]
    assert np.isclose(100, result)












