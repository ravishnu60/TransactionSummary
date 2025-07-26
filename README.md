# Transaction Summary

This is a simple API to return a transaction summary from a PDF file using [FastAPI](https://fastapi.tiangolo.com/) and [Google Gemini API](https://ai.google.dev/gemini-api/docs).

## Installation

1. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a .env file with below environment variables:

    ```bash
    GOOGLE_KEY=YOUR_GOOGLE_KEY
    MODEL_NAME=YOUR_MODEL_NAME
    ```

## Usage

1. Start the FastAPI server:

    ```bash
    fastapi main.py --port 8000
    ```

2. Swagger UI will be available at http://localhost:8000/docs

3. Make a request to the API:

    ```bash
    Method: POST
    URL: http://localhost:8000/summary
    Headers: Content-Type: multipart/form-data
    Form Data: file: (PDF file)
    ```

4. The API will return a JSON response with the transaction summary.