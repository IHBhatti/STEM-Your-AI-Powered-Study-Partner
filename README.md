# STEM-Your-AI-Powered-Study-Partner
# Introduction
STEM can read multiple textbooks at once and answer queries in a conversational style, just like GPT — but with the accuracy of grounded knowledge.
It’s like having a study partner that never gets tired of flipping pages!
# Features
Upload and process multiple textbooks (PDFs)
Splits content into chunks for efficient retrieval
Uses FAISS + embeddings for accurate knowledge search
Answers questions in natural, conversational style
Ensures responses are always grounded in your uploaded textbooks
Clean Streamlit UI with real-time chat interface
# Tech Stack
Python 3.9+
Streamlit
 – interactive UI
LangChain
 – text processing & retrieval
FAISS
 – similarity search
[OpenAI / Hugging Face Models] 
  – conversational AI
[PDFMiner / PyPDF2] 
  – PDF text extraction
# Project Structure
📦 STEM
├── app/
│   ├── ui.py                  # Streamlit UI components
│   ├── pdf_utils.py           # Extract text from PDFs
│   ├── vectorstore_utils.py   # FAISS index creation & retrieval
│   ├── chat_utils.py          # Chat model & response generation
│   └── config.py              # API keys & configuration
├── main.py                    # Entry point (Streamlit app)
├── requirements.txt           # Dependencies
# Conclusion
STEM brings the power of AI + RAG to education — a tool that helps students, researchers, and professionals get instant, accurate answers from their study materials. Think of it as a personal AI tutor that never gets tired.
