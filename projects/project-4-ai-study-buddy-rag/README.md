# Project 4 — AI Study Buddy with RAG

A compact retrieval-augmented generation project for studying from PDFs.

## Pipeline

1. Extract text from an uploaded PDF.
2. Split the text into overlapping chunks.
3. Create embeddings for each chunk.
4. Embed the user's question.
5. Rank chunks with cosine similarity.
6. Send the best context to the chat model for a grounded answer.

## What it demonstrates

- PDF extraction
- Text chunking
- Embeddings and cosine similarity
- Retrieval-augmented generation
- Safe environment-variable configuration
- Flask request handling

The public portfolio demo uses a client-side retrieval simulation so visitors can try the concept without exposing an API key.
