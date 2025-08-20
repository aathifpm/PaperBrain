import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

class VectorStore:
    def __init__(self, embedding_model="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize FAISS vector store with sentence transformer embeddings.
        
        Args:
            embedding_model: Name of the sentence transformer model
        """
        try:
            self.embedder = SentenceTransformer(embedding_model)
        except Exception as e:
            print(f"Error loading model {embedding_model}: {e}")
            print("Falling back to 'all-MiniLM-L6-v2' model...")
            # Try alternative model names
            try:
                self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception as e2:
                print(f"Error loading fallback model: {e2}")
                print("Using paraphrase-MiniLM-L6-v2 as final fallback...")
                self.embedder = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.embeddings = []
    
    def add_documents(self, documents):
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects with page_content and metadata
        """
        # Extract texts
        texts = [doc.page_content for doc in documents]
        
        # Generate embeddings
        new_embeddings = self.embedder.encode(texts, show_progress_bar=False)
        
        # Add to FAISS index
        self.index.add(np.array(new_embeddings).astype('float32'))
        
        # Store documents and embeddings
        self.documents.extend(documents)
        self.embeddings.extend(new_embeddings)
    
    def search(self, query, k=5):
        """
        Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of tuples (document, score)
        """
        if len(self.documents) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedder.encode([query], show_progress_bar=False)
        
        # Search in FAISS
        k = min(k, len(self.documents))  # Ensure k doesn't exceed number of documents
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            k
        )
        
        # Return documents with scores
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:  # Valid index
                results.append({
                    'document': self.documents[idx],
                    'score': float(distances[0][i])
                })
        
        return results
    
    def clear(self):
        """Clear all documents from the vector store."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.embeddings = []
    
    def save(self, path):
        """Save vector store to disk."""
        data = {
            'documents': self.documents,
            'embeddings': self.embeddings,
            'index': faiss.serialize_index(self.index)
        }
        with open(path, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, path):
        """Load vector store from disk."""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.documents = data['documents']
        self.embeddings = data['embeddings']
        self.index = faiss.deserialize_index(data['index'])