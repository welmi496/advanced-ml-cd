from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType


texts = [
    "I love this movie",
    "This is amazing",
    "What a great experience",
    "I am very happy",
    "Excellent product",
    "This is good",
    "I hate this movie",
    "This is terrible",
    "What a bad experience",
    "I am very disappointed",
    "Awful product",
    "This is horrible"
]

labels = [
    "positive",
    "positive",
    "positive",
    "positive",
    "positive",
    "positive",
    "negative",
    "negative",
    "negative",
    "negative",
    "negative",
    "negative"
]

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

model.fit(texts, labels)

initial_type = [
    ("input", StringTensorType([None, 1]))
]

onnx_model = convert_sklearn(
    model,
    initial_types=initial_type
)

with open("model/model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("Model created successfully: model/model.onnx")
