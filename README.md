# Advanced ML Continuous Delivery Assignment

## Project Overview

This project demonstrates a Continuous Integration and Continuous Delivery (CI/CD) workflow for a machine learning sentiment analysis application.

The application uses:

* FastAPI for serving the machine learning model
* ONNX Runtime for model inference
* Docker for containerization
* Pytest for automated testing
* GitHub Actions for CI/CD automation

The sentiment analysis model classifies text as either positive or negative.

---

## Project Structure

```text
advanced-ml-cd/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── model_service.py
│
├── model/
│   └── model.onnx
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_api.py
│
├── Dockerfile
├── requirements.txt
├── train_sentiment_model.py
├── README.md
├── .gitignore
└── .dockerignore
```

---

## Prerequisites

The following tools are required:

* Python 3.11
* pip
* Docker Desktop
* Git
* GitHub account

---

## Create a Virtual Environment

Create a Python virtual environment:

```bash
python3.11 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

---

## Install Dependencies

Install all project dependencies:

```bash
python -m pip install -r requirements.txt
```

Main dependencies include:

* FastAPI
* Uvicorn
* ONNX Runtime
* NumPy
* Scikit-learn
* skl2onnx
* Pytest
* HTTPX

---

## Machine Learning Model

The project uses a small sentiment analysis model created with:

* TF-IDF Vectorization
* Logistic Regression
* Scikit-learn

The trained model is exported to ONNX format and stored at:

```text
model/model.onnx
```

To regenerate the model, run:

```bash
python train_sentiment_model.py
```

---

## Run the FastAPI Application

Start the API locally with:

```bash
python -m uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

The automatically generated API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Root Endpoint

```text
GET /
```

Returns a message confirming that the API is running.

### Health Check

```text
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Sentiment Prediction

```text
POST /predict
```

Example request:

```json
{
  "text": "I love this movie"
}
```

Example response:

```json
{
  "text": "I love this movie",
  "sentiment": "positive",
  "confidence": 0.74
}
```

The exact confidence value may vary depending on the trained model.

---

## Automated Testing

The project includes automated tests for:

* Root endpoint
* Health endpoint
* Positive sentiment prediction
* Negative sentiment prediction
* Empty input
* Missing input
* Invalid input types
* Long text inputs
* Special characters
* Malicious input
* Concurrent requests

Run the test suite with:

```bash
python -m pytest tests -v
```

The tests verify the reliability and robustness of the API before deployment.

---

## Docker

The application is containerized using Docker.

Build the Docker image:

```bash
docker build -t advanced-ml-cd:1.0 .
```

Run the container:

```bash
docker run --name advanced-ml-cd-container -p 8000:8000 advanced-ml-cd:1.0
```

The API can then be accessed at:

```text
http://127.0.0.1:8000
```

Docker API documentation:

```text
http://127.0.0.1:8000/docs
```

The Dockerfile uses a multi-stage build and a minimal Python 3.11 image.

Locale support is installed in the runtime container because the ONNX text processing operations require the `en_US.UTF-8` locale.

---

## CI/CD Pipeline

GitHub Actions is used for Continuous Integration and Continuous Delivery.

The workflow file is located at:

```text
.github/workflows/ci.yml
```

The workflow is automatically triggered when code is pushed to the `main` branch.

The pipeline performs the following steps:

1. Checks out the GitHub repository
2. Configures Python 3.11
3. Installs locale support
4. Installs Python dependencies
5. Runs automated tests
6. Builds the Docker image
7. Runs the Docker container
8. Waits for the API to start
9. Tests the `/health` endpoint
10. Displays the container logs

A failed test or build prevents the pipeline from completing successfully.

---

## Testing Strategy

The project includes several forms of automated testing.

### Functional Testing

Functional tests verify that sentiment prediction works correctly for positive and negative inputs.

### Edge Case Testing

The API is tested with:

* Empty text
* Very long text
* Special characters
* Missing input values

### Invalid and Malicious Input Testing

The API is tested with invalid data types and malicious-looking text such as script tags.

These tests help verify that the API handles unexpected input safely.

### Concurrency Testing

Multiple API requests are sent concurrently using Python's `ThreadPoolExecutor`.

This verifies that the application can process multiple requests without failing.

### Integration Testing

The GitHub Actions pipeline builds and starts the Docker container, then sends a request to the `/health` endpoint.

This verifies that the complete application works correctly inside the deployment environment.

---

## Challenges Faced

### Python Environment Conflict

The computer had both Anaconda Python 3.13 and a Python 3.11 virtual environment.

At first, Uvicorn used the Anaconda Python installation and could not locate ONNX Runtime.

The issue was solved by running Uvicorn through the virtual environment:

```bash
python -m uvicorn app.main:app --reload
```

### Missing ONNX Model

The original sentiment ONNX model was not available locally.

A small sentiment analysis model was trained using TF-IDF and Logistic Regression and exported to ONNX format using `skl2onnx`.

### Docker Locale Error

The ONNX model initially failed inside the Docker container because the minimal Linux image did not contain the `en_US.UTF-8` locale.

Locale support was added to the Dockerfile and the required environment variables were configured.

### Git Repository Cleanup

The `.venv` directory was accidentally tracked during the initial Git commit.

A `.gitignore` file was configured and the virtual environment and cache files were removed from Git tracking.

### GitHub Actions Workflow Issue

The initial GitHub Actions workflow failed because the workflow file was empty.

After adding the complete workflow configuration, the CI/CD pipeline successfully executed the tests and Docker deployment checks.

---

## Repository

GitHub repository:

```text
https://github.com/welmi496/advanced-ml-cd
```

---

## Conclusion

This project demonstrates how CI/CD practices can be applied to machine learning systems.

The final implementation includes:

* A FastAPI ML inference service
* An ONNX sentiment analysis model
* Automated testing
* Docker containerization
* GitHub Actions CI/CD automation
* Health checks
* Basic concurrency and robustness testing

The CI/CD pipeline improves reliability by automatically testing the application and validating the Docker deployment whenever changes are pushed to the main branch.
