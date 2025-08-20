import os
import google.generativeai as genai
from typing import List, Tuple

class RAGChain:
    def __init__(self, model_name="gemini-2.0-flash"):
        """
        Initialize RAG chain with Gemini Pro.
        
        Args:
            model_name: Name of the Gemini model to use
        """
        # Configure Gemini
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Please set GOOGLE_API_KEY environment variable")
        
        genai.configure(api_key=api_key)
        
        # Configure generation settings
        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 0.1,
        }
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
        
        # System prompt template
        self.system_prompt = """You are a helpful assistant that answers questions based on the provided context.

IMPORTANT RULES:
1. Use ALL relevant information from the provided context to give comprehensive answers
2. If the answer spans multiple chunks, combine and synthesize the information
3. When the question asks for components, features, or details, provide ALL available information
4. Organize your answer logically with clear structure (use headings, bullet points, or numbered lists when helpful)
5. When citing information, mention which document and chunk it comes from
6. If some information is missing, say "Additional information may be available in other parts of the document"
7. Do not make up or hallucinate information not found in the context

Context (multiple chunks may contain related information):
{context}

Question: {question}

Provide a comprehensive answer using all relevant information from the context above:"""
    
    def generate_answer(self, question: str, search_results: List[dict]) -> Tuple[str, List[dict]]:
        """
        Generate an answer using retrieved documents.
        
        Args:
            question: User's question
            search_results: List of search results from vector store
            
        Returns:
            Tuple of (answer, sources)
        """
        # Prepare context from search results
        context_parts = []
        sources = []
        
        for i, result in enumerate(search_results):
            doc = result['document']
            context_parts.append(
                f"[Document: {doc.metadata['source']}, Chunk {doc.metadata['chunk_id']}]\n"
                f"{doc.page_content}\n"
            )
            sources.append({
                'doc': doc.metadata['source'],
                'chunk': doc.metadata['chunk_id'],
                'text': doc.page_content
            })
        
        context = "\n---\n".join(context_parts)
        
        # Create prompt
        prompt = self.system_prompt.format(
            context=context,
            question=question
        )
        
        # Generate response
        try:
            response = self.model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"Error generating response: {str(e)}"
        
        return answer, sources
    
    def generate_answer_with_history(self, question: str, search_results: List[dict], 
                                   chat_history: List[dict]) -> Tuple[str, List[dict]]:
        """
        Generate an answer considering chat history.
        
        Args:
            question: User's question
            search_results: List of search results
            chat_history: Previous chat messages
            
        Returns:
            Tuple of (answer, sources)
        """
        # Build conversation context
        history_context = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in chat_history[-5:]  # Last 5 messages for context
        ])
        
        # Modify question to include history context
        enhanced_question = f"""Previous conversation:
{history_context}

Current question: {question}"""
        
        return self.generate_answer(enhanced_question, search_results)