# Project 1 — AI Chat Web App

A compact Flask project that connects a browser-based chat interface to an Azure OpenAI deployment.

## What it demonstrates

- Flask routes and JSON APIs
- Browser-to-server requests with `fetch`
- Environment-variable based secret handling
- AI-assisted product development
- Error handling and a clean chat interface

## Run locally

1. Install `flask`, `openai`, and `python-dotenv`.
2. Set `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, and `AZURE_OPENAI_DEPLOYMENT` in your environment.
3. Run `python app.py`.
4. Open `http://localhost:5000`.

The public portfolio demo uses a browser-only simulation so no API key is exposed.
