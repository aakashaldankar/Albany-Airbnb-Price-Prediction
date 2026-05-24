from app.prediction_pipeline import predict, pre_process
import numpy as np
import pandas as pd


def test_predict(monkeypatch):

    calls={
        "pre_process": False,
        "predict": False
    }

    class MockRequest:

        def model_dump(self):
            return {"feature1": 10,"feature2": 11}
        
    def mock_pre_process(data):
        calls['pre_process']=True
        return data
    
    class MockModel:

        def predict(self, data_df):

            assert isinstance(data_df, pd.DataFrame)
            assert data_df.shape[0]==1

            calls["predict"]=True
            return np.array([np.log1p(100)])
        
    monkeypatch.setattr("app.prediction_pipeline.pre_process", mock_pre_process)
    monkeypatch.setattr("app.prediction_pipeline.model", MockModel())

    result=predict(MockRequest())

    assert calls["predict"]
    assert calls["pre_process"]
    assert np.isclose(100, result)












