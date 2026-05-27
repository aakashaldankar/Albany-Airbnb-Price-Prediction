from app.prediction_pipeline import prediction
import numpy as np

def test_prediction_pipeline(prediction_request):

    calls={"predict": False}
    
    request=prediction_request

    class MockModel:

        def predict(self, df):
            assert df.shape[0]==1
            calls["predict"]=True
            return [np.log1p(100)]

    result=prediction(request, model=MockModel())

    assert np.isclose(100, result)
    assert calls["predict"]


    


