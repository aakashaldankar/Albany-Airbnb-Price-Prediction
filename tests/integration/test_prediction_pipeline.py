from app.prediction_pipeline import prediction
import numpy as np
import pandas as pd

def test_prediction_pipeline(prediction_request, monkeypatch):

    calls={"predict": False}
    
    request=prediction_request

    def mock_pre_process(data, encoders):
        return {"feature1":[1],"feature2":[2]}

    class MockModel:

        def predict(self, df):
            assert df.shape[0]==1
            calls["predict"]=True
            return [np.log1p(100)]
        
    monkeypatch.setattr('app.prediction_pipeline.pre_process',mock_pre_process)
    
    encoders={'ohe_one': 1, 'target_encoding':2}  
    result=prediction(request, model=MockModel(), encoders=encoders)

    assert np.isclose(10, result)
    assert calls["predict"]==False


    


