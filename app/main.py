from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.model_service import predict_sentiment


app = FastAPI(
    title="Advanced ML CD - Sentiment Analysis API",
    description="FastAPI application for serving an ONNX sentiment analysis model.",
    version="1.0.0"
)


class SentimentRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text to analyze for sentiment"
    )


@app.get("/")
def root():
    return {
        "message": "Advanced ML CD Sentiment Analysis API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(request: SentimentRequest):
    prediction = predict_sentiment(request.text)

    return {
        "text": request.text,
        "sentiment": prediction["sentiment"],
        "confidence": prediction["confidence"]
    }
