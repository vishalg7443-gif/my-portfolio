import os
from io import BytesIO

import numpy as np
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import AzureOpenAI
from pypdf import PdfReader

load_dotenv()

app = Flask(__name__)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
)
CHAT_MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5-nano")
EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

store = {"chunks": [], "embeddings": None, "filename": ""}


def extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()


def chunk_text(text: str, size: int = 700, overlap: int = 100) -> list[str]:
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return np.array([item.embedding for item in response.data], dtype=float)


def cosine_top_k(query_vector: np.ndarray, matrix: np.ndarray, k: int = 3) -> list[int]:
    q_norm = np.linalg.norm(query_vector)
    row_norms = np.linalg.norm(matrix, axis=1)
    denom = row_norms * q_norm
    scores = np.divide(matrix @ query_vector, denom, out=np.zeros_like(row_norms), where=denom != 0)
    return np.argsort(-scores)[:k].tolist()


@app.post("/upload")
def upload():
    file = request.files.get("file")
    if not file or not file.filename.lower().endswith(".pdf"):
        return jsonify(error="Upload a PDF file"), 400

    text = extract_pdf(file.read())
    chunks = chunk_text(text)
    if not chunks:
        return jsonify(error="No readable text found"), 400

    store["filename"] = file.filename
    store["chunks"] = chunks
    store["embeddings"] = embed(chunks)
    return jsonify(filename=file.filename, chunks=len(chunks))


@app.post("/ask")
def ask():
    question = (request.get_json(silent=True) or {}).get("question", "").strip()
    if not question:
        return jsonify(error="Question is required"), 400
    if not store["chunks"] or store["embeddings"] is None:
        return jsonify(error="Upload a PDF first"), 400

    q_vector = embed([question])[0]
    indexes = cosine_top_k(q_vector, store["embeddings"], k=3)
    sources = [store["chunks"][i] for i in indexes]
    context = "\n\n---\n\n".join(sources)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "Answer only from the provided context. If the answer is not present, say you do not know from this document.",
            },
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return jsonify(answer=response.choices[0].message.content, sources=sources)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
