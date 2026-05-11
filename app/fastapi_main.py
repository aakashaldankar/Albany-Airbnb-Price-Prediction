from fastapi import FastAPI
from app.prediction_pipeline import predict
from app.schemas import PredictionRequest, PredictionResult

app=FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionResult)
def predict_price(request: PredictionRequest):
    prediction=predict(request)
    return PredictionResult(result=prediction)
