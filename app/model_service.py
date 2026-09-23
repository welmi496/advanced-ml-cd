import onnxruntime as ort
import numpy as np

MODEL_PATH = "model/model.onnx"

session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)


def predict_sentiment(text: str):
    input_data = np.array([[text]], dtype=object)

    results = session.run(
        None,
        {
            "input": input_data
        }
    )

    label = results[0][0]
    probabilities = results[1][0]

    confidence = probabilities[label]

    return {
        "sentiment": label,
        "confidence": float(confidence)
    }
