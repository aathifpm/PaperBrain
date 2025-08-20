# MinimalRAG - Lightweight NotebookLM Clone

A minimal Retrieval-Augmented Generation (RAG) chatbot that lets you upload documents and ask questions about them.

## Features

- 📄 Document upload (PDF, TXT, DOCX)
- 🔍 Semantic search using embeddings
- 💬 Chat interface with context-aware responses
- 📍 Source attribution for answers
- 💾 Local vector storage with FAISS

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API key:
```bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
```

3. Run the app:
```bash
streamlit run app.py
```

## Tech Stack

- **Frontend**: Streamlit
- **Vector DB**: FAISS
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: Google Gemini Pro
- **Document Processing**: LangChain

## Usage

1. Upload one or more documents using the sidebar
2. Wait for processing to complete
3. Start asking questions in the chat interface
4. View answers with source references

## Project Structure

```
minimal-rag/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document ingestion and chunking
├── vector_store.py       # FAISS vector store management
├── rag_chain.py          # RAG logic and LLM integration
├── requirements.txt      # Dependencies
└── README.md            # This file
```