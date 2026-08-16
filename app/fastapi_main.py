from fastapi import FastAPI, HTTPException, Depends
from app.schemas import PredictionRequest, PredictionResult
from app.model_loader import load_model, MODEL_NAME, MODEL_ALIAS, get_model_version

app=FastAPI()

def get_predictor():
    from app.prediction_pipeline import prediction
    return prediction

@app.get("/health")
def health():

    try:
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction Failed")


@app.post("/admin/reload")
def reload_model():

    try:
        load_model()
        return {
            "status": "reloaded",
            "model_name": MODEL_NAME,
            "model_alias": MODEL_ALIAS,
            "version": get_model_version(),
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Reload Failed")


@app.post("/predict", response_model=PredictionResult)
def predict_price(request: PredictionRequest, predictor=Depends(get_predictor)):

    try: 
        prediction=predictor(request)
        return PredictionResult(result=prediction)
    except Exception:
        raise HTTPException(status_code=500, detail="Prediction Failed")
