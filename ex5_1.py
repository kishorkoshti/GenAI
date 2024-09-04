from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
import tempfile

st.title("PDF Uploader and Reader")

# File uploader for PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

#print(uploaded_file.getvalue())
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text = "This is a test document."
query_result = embeddings.embed_query(text)
#print(query_result)
if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name
    
    st.write(f"Temporary file path: {tmp_file_path}")
    loader = PyPDFLoader(tmp_file_path)
    pages = loader.load_and_split()
    query_result = embeddings.embed_query(pages)
    print(query_result)

    




#loader = PyPDFLoader(uploaded_file['upload_url'])
#pages = loader.load_and_split()ex