import streamlit as st
from app.ui import pdf_uploader
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrieve_relevant_docs
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time

st.set_page_config(
    page_title="STEM GPT",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""
<style>
      .chat-message{
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
      }
      .chat-message.user{
        background-color: #2b313e;
        color:white;
      }
      .chat-message.assitant{
        background-color: #475063;
        color:black;
      }
      .chat-message.avatar{
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        margin-right: 0.5rem;
      }
      .chat-message.message{
        flex:1;
      }
      .chat-message.timestamp{
        font-size: 0.8rem;
        capacity: 0.7;
        margin-top: 0.5rem;
      }
      .stbutton>button{
        background-color: #475063;
        color:white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
      }
      .stbutton>button:hover{
        background-color: #2b313e;
      }
      .upload-section{
        background-color: #2b313e;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
      }
      .status-success{
        background-color: #475063;
        color:#155724;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem e;
      }

</style>
  """, unsafe_allow_html=True)

if "message" not in st.session_state:
    st.session_state.message = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore= None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None


st.markdown("""
<div style="text-align: center; padding=2rem 0;">
    <h1 style="color:#ff4b4b; font-size: 3rem; margin-bottom:0.5rem;">STEM GPT</h1>
    <p style="font-size:1.2rem; color: #666; margin-bottom: 2rem;">Your Intelligent STBB Assistant</p>
</div>
""", unsafe_allow_html=True)


# sidebar for doccument upload
with st.sidebar:
  st.markdown('### 📂 Upload Document')
  st.markdown('upload your sttb document to start chatting!')
  uploaded_files = pdf_uploader()
  if uploaded_files:
    st.success(f"📄{len(uploaded_files)} document(s) uploaded successfully!")
    # process documents
    if st.button("🚀 process documents", type="primary"):
      with st.spinner("Processing STTB documents..."):
        # Extract text from all documents
        all_texts = []
        for file in uploaded_files:
          text = extract_text_from_pdf(file)
          all_texts.append(text)
        # Splits text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
          chunk_size=1000,
          chunk_overlap=200,
          length_function=len
        )
        chunks = []
        for text in all_texts:
          chunks.extend(text_splitter.split_text(text))
        # Create FAISS index
        vectorstore = create_faiss_index(chunks)
        st.session_state.vectorstore = vectorstore
        st.success("✅ Document processing completed!")
        # Initialize the Chat Model
        chat_model = get_chat_model(EURI_API_KEY)
        st.session_state.chat_model = chat_model
        st.success("✅ Documents processed successfully!")
        st.balloons()
# Main Chat Interface
st.markdown('### 💬 Chat with your STTB books')
# Display Chat Message
for message in st.session_state.message:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])
    st.caption(message["timestamp"])
# Chat Input
if prompt := st.chat_input("Ask about your STTB books...."):
  # Add user message to chat history
  timestamp = time.strftime("%H:%M")
  st.session_state.message.append({
      "role": "user",
      "content": prompt,
      "timestamp":timestamp
  })
  # Display user message
  with st.chat_message("user"):
    st.markdown(prompt)
    st.caption(timestamp)
  # Generate Responce
  if st.session_state.vectorstore and st.session_state.chat_model:
    with st.chat_message("assistant"):
      with st.spinner("Generating response..."):
        # retrieve relevant document
        relevant_docs = retrieve_relevant_docs(st.session_state.vectorstore, prompt)
        # create content from relevant document
        context="\n\n".join([doc.page_content for doc in relevant_docs])
        # Create prompt with context
        system_prompt= f"""" You are STEM GPT, an intelligent STTB document assistant.
        Based on the following STTB documents, provide accurate and helpful answers.
        If the information is not in the documents, clearly state that.

        STTB Documents:
        {context}
        user question: {prompt}


        Answer:"""

        response = ask_chat_model(st.session_state.chat_model, system_prompt)
        # Display assistant response
      st.markdown(response)
      st.caption(timestamp)
      # add assistant message to chat history
      st.session_state.message.append({
          "role": "assistant",
          "content": response,
          "timestamp":timestamp
      })
  else:
    with st.chat_message("Assistant"):
      st.error("⚠ please upload and process the document first!")
      st.caption(timestamp)
# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color:#666; font-size:0.9 rem;>
<p>Powered by EURI AI and Langchain</p>
</dive>
""", unsafe_allow_html=True)


