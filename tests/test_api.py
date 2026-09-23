from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_positive_prediction():
    response = client.post(
        "/predict",
        json={"text": "I love this movie"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sentiment"] == "positive"
    assert 0 <= data["confidence"] <= 1


def test_negative_prediction():
    response = client.post(
        "/predict",
        json={"text": "This is terrible and awful"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sentiment"] == "negative"
    assert 0 <= data["confidence"] <= 1


def test_empty_input():
    response = client.post(
        "/predict",
        json={"text": ""}
    )

    assert response.status_code == 422


def test_missing_text_field():
    response = client.post(
        "/predict",
        json={}
    )

    assert response.status_code == 422


def test_invalid_input_type():
    response = client.post(
        "/predict",
        json={"text": 12345}
    )

    assert response.status_code == 422


def test_long_input():
    long_text = "good " * 300

    response = client.post(
        "/predict",
        json={"text": long_text}
    )

    assert response.status_code == 422


def test_special_characters():
    response = client.post(
        "/predict",
        json={
            "text": "!@#$%^&*()_+{}[]<>???"
        }
    )

    assert response.status_code == 200


def test_malicious_input():
    malicious_text = "<script>alert('test')</script>"

    response = client.post(
        "/predict",
        json={"text": malicious_text}
    )

    assert response.status_code == 200

    data = response.json()

    assert "sentiment" in data
    assert "confidence" in data


def send_request(text):
    return client.post(
        "/predict",
        json={"text": text}
    )


def test_concurrent_requests():
    texts = [
        "I love this movie",
        "This is terrible",
        "Great experience",
        "Awful product",
        "I am very happy",
        "I hate this",
        "Excellent service",
        "Bad experience",
        "Amazing movie",
        "Horrible product"
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        responses = list(
            executor.map(send_request, texts)
        )

    for response in responses:
        assert response.status_code == 200
