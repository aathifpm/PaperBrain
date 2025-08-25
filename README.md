# 📚 PaperBrain - AI-Powered Document Intelligence

> **Transform your documents into intelligent, searchable knowledge with advanced RAG technology**

PaperBrain is a cutting-edge **Retrieval-Augmented Generation (RAG)** chatbot that allows seamless document uploads and delivers AI-powered, contextually-aware answers. With advanced semantic search and vector embeddings, PaperBrain makes your documents interactive, searchable, and easy to explore.

---
Demo: https://paperbrain.streamlit.app
## ✨ Highlights

### 🎯 **Core Features**
- 📄 **Multi-format document support** (PDF, TXT, DOCX)
- 🔍 **Semantic search** with state-of-the-art embeddings
- 💬 **Conversational AI** with contextual responses
- 📍 **Source attribution** for every response
- ⚡ **Real-time document processing** and instant querying

### 🚀 **Advanced Capabilities**
- 💾 **Local FAISS vector storage** for fast similarity search
- 🧠 **Context preservation** with conversation memory
- 📊 **Semantic text chunking** for optimized retrieval
- 🎨 **Streamlit-powered interface** for user-friendly interaction

---

## 🛠️ Technology Stack

### 🤖 **AI & Machine Learning**
| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | 🟢 Google Gemini Pro | Human-like responses & reasoning |
| **Embeddings** | 🔵 Sentence Transformers *(all-MiniLM-L6-v2)* | Semantic text encoding |
| **Text Processing** | 🟡 LangChain | Document chunking & prompt engineering |

### 💻 **Backend & Storage**
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Vector DB** | 🟣 FAISS | High-performance nearest neighbor search |
| **Web Framework** | 🔴 Streamlit | Interactive web UI |
| **Language** | 🐍 Python | Core backend logic |

### 🔧 **Supporting Tools**
- Document loaders: PDF, TXT, DOCX
- Intelligent text splitters
- Local vector store management
- Conversation memory management

---

## 🚀 Quick Start

### 📋 Prerequisites
- Python 3.8+
- Google API Key (Gemini Pro)

### ⚙️ Installation
```bash
# Clone repository
git clone https://github.com/aathifpm/PaperBrain.git
cd PaperBrain

# Install dependencies
pip install -r requirements.txt

# Configure API credentials
echo "GOOGLE_API_KEY=your-gemini-api-key" > .env

# Run the application
streamlit run app.py
```

---

📖 Usage Guide

📤 Upload Documents

1. Open the sidebar in the Streamlit interface
2. Upload or drag-and-drop .pdf, .txt, .docx files
3. Wait for processing to complete

💬 Ask Questions

1. Use the chatbox to query your documents
2. Get AI-generated responses with document references
3. Enjoy context-aware conversation flow

---

🏗️ Project Structure
```
PaperBrain/
├── app.py                  # Main Streamlit app
├── document_processor.py   # Handles ingestion & chunking
├── vector_store.py         # FAISS vector storage
├── rag_chain.py            # RAG pipeline logic
├── requirements.txt        # Dependencies
├── .env                    # API credentials
└── README.md               # Documentation

```
---

🔬 Technical Highlights
```
🧠 RAG Pipeline: Chunking → Embeddings → FAISS Retrieval → LLM
🔍 Semantic Embeddings: Sentence Transformers for context-rich queries
⚡ FAISS Optimization: High-speed similarity search
🧩 LangChain Integration: Prompt orchestration & context injection
🤖 Gemini Pro LLM: Generates natural, reasoning-rich responses
```
---

🚧 Future Enhancements
```
[ ] 🌍 Multi-language support
[ ] 📊 Support for PPTX, XLSX
[ ] ☁️ Cloud storage integration (Google Drive, Dropbox)
[ ] 🔐 User authentication for multi-user access
[ ] 📑 Export chat history & summaries
[ ] 📈 Document usage analytics
```

---

🤝 Contributing

Contributions are welcome!
Submit issues, ideas, or pull requests to make PaperBrain even better.

---

📄 License

This project is open source. Refer to the repository for details.

---

⭐ If you like this project, consider giving it a star on GitHub!

---
