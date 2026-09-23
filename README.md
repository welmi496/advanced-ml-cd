# Advanced ML Continuous Delivery - ONNX Sentiment API

This repository is my student implementation of a Continuous Delivery assignment for a machine-learning model. The project serves a pre-trained ONNX sentiment-analysis model through FastAPI, packages the service with Docker, and validates it automatically with GitHub Actions.

# Project structure

advanced-ml-cd/
├── app/
│   ├── __init__.py
│   └── main.py
├── model/
│   └── README.md
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .github/workflows/
│   └── cicd.yml
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── .dockerignore
├── .gitignore
└── README.md

# Main features

FastAPI REST API with /health and /predict endpoints.

ONNX Runtime inference for a sentiment model.

Input validation with Pydantic.

Thread-pool execution for inference so requests do not block FastAPI's event loop.

Gunicorn with multiple Uvicorn workers for concurrent requests.

Multi-stage Docker build and non-root runtime user.

Functional, edge-case, robustness, integration, and concurrent-request tests.

GitHub Actions workflow that runs tests, builds the image, starts the container, checks health, and performs a prediction smoke test.

# Prerequisites

Python 3.11+

Docker Desktop

Git

GitHub account

The pre-trained ONNX sentiment model supplied in the lab

# 1. Add the ONNX model

Copy the provided model into:

model/model.onnx

The default tokenizer is:

distilbert-base-uncased-finetuned-sst-2-english

If the ONNX model was exported from another transformer, set TOKENIZER_NAME to the correct Hugging Face tokenizer before running the API.

# 2. Run locally with Python

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

Start the application:

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Open the interactive API documentation at http://127.0.0.1:8000/docs.

Health check:

curl http://127.0.0.1:8000/health

Prediction example:

curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"I really enjoyed this product."}'

Example response:

{
  "label": "POSITIVE",
  "confidence": 0.98
}

# 3. Run tests

The automated test suite uses a deterministic mock sentiment model so CI does not require committing the lab's ONNX file.

USE_MOCK_MODEL=true pytest -q

The tests cover:

Valid positive and negative inputs.

Blank and missing inputs.

Incorrect data types.

Oversized text.

Script-like and SQL-like strings.

Multiple concurrent prediction requests.

Health and root endpoints.

# 4. Build and run with Docker

Build the image:

docker build -t advanced-ml-cd:1.0 .

Run with the real ONNX model:

docker run --rm -p 8000:8000 advanced-ml-cd:1.0

For a CI-style smoke test without the real model:

docker run --rm -e USE_MOCK_MODEL=true -p 8000:8000 advanced-ml-cd:1.0

# 5. GitHub Actions CI/CD

The workflow is stored at .github/workflows/cicd.yml. It runs automatically on pushes and pull requests to main.

Pipeline stages:

Check out the repository.

Install Python dependencies.

Run automated tests.

Build the Docker image.

Start a container in mock mode.

Verify /health.

Send a real HTTP request to /predict.

Print container logs if a stage fails.

Clean up the container.

A failed test or failed integration check stops the pipeline before the image can be considered ready for delivery.

# 6. Creating the GitHub repository

Create a public or private GitHub repository called advanced-ml-cd, then run:

git init
git add .
git commit -m "Initial advanced ML CD assignment"
git branch -M main
git remote add origin https://github.com/welmi496/advanced-ml-cd.git
git push -u origin main

Replace WELMI496 with your GitHub username.

# Security and reliability considerations

Requests are validated before inference.

The container runs as a non-root user.

Model inference is isolated from user input; text is never executed as code or SQL.

Large input is rejected to reduce accidental or malicious resource exhaustion.

The health endpoint can be used by container orchestrators and monitoring systems.

Application/container logs can be collected centrally in production.

Production systems should add authentication, HTTPS, rate limiting, model/data-drift monitoring, and a controlled rollback strategy.

# Blue-green / canary deployment extension

The container is immutable and therefore suitable for either blue-green or canary deployment. For a critical healthcare system, I would use a carefully controlled blue-green process for the final production switch, combined with strong validation, clinical governance, and immediate rollback capability. Canary deployment can also be useful before the full switch when organizational and safety controls permit exposure to a limited traffic segment.
