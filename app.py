import streamlit as st
import os
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from vector_store import VectorStore
from rag_chain import RAGChain
import tempfile

# Load environment variables from .env file
load_dotenv()

# Page config
st.set_page_config(
    page_title="PaperBrain",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = VectorStore()
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = RAGChain()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'document_count' not in st.session_state:
    st.session_state.document_count = 0

# Title and description
st.title("📚 PaperBrain - Your documents, AI-powered answers")
st.markdown("Upload documents and ask questions about them!")

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Upload")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['pdf', 'txt', 'docx'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Process Documents", type="primary"):
            with st.spinner("Processing documents..."):
                processor = DocumentProcessor()
                
                for uploaded_file in uploaded_files:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        tmp_path = tmp_file.name
                    
                    # Process document
                    chunks = processor.process_document(tmp_path, uploaded_file.name)
                    
                    # Add to vector store
                    st.session_state.vector_store.add_documents(chunks)
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                
                st.session_state.document_count += len(uploaded_files)
                st.success(f"✅ Processed {len(uploaded_files)} document(s)")
    
    # Document status
    st.divider()
    st.metric("Documents in Knowledge Base", st.session_state.document_count)
    
    # Clear all button
    if st.button("Clear All Data"):
        st.session_state.vector_store = VectorStore()
        st.session_state.messages = []
        st.session_state.document_count = 0
        st.rerun()

# Main chat interface
st.header("💬 Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📍 Sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['doc']}** (chunk {source['chunk']})")
                    st.text(source['text'][:200] + "...")

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    if st.session_state.document_count == 0:
        st.warning("Please upload and process documents first!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Get relevant chunks (increased to get more comprehensive information)
                relevant_chunks = st.session_state.vector_store.search(prompt, k=15)
                
                if relevant_chunks:
                    # Generate answer
                    response, sources = st.session_state.rag_chain.generate_answer(
                        prompt, 
                        relevant_chunks
                    )
                    
                    st.markdown(response)
                    
                    # Show sources
                    with st.expander("📍 Sources"):
                        for source in sources:
                            st.markdown(f"**{source['doc']}** (chunk {source['chunk']})")
                            st.text(source['text'][:200] + "...")
                    
                    # Add to message history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources": sources
                    })
                else:
                    response = "I couldn't find relevant information in the uploaded documents to answer your question."
                    st.markdown(response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })