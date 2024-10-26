import os
import io
import shutil
import tempfile
from dotenv import load_dotenv
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_PATH = "vector_db_dir"
load_dotenv()

# PDF Loader
def get_pdf_docs(pdf_docs):
    all_docs = []
    for pdf in pdf_docs:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Write the contents of the uploaded file to the temporary file
            temp_file.write(pdf.read())
            temp_file_path = temp_file.name

        loader = PyPDFLoader(temp_file_path)
        docs = loader.load()
        all_docs.extend(docs)

        os.remove(temp_file_path) #remove temp file

    return all_docs

def create_db_for_pdf_docs(all_docs):
    chromadb.api.client.SharedSystemClient.clear_system_cache()

    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(all_docs)
    
    print(f'Splitted {len(all_docs)} documents into {len(splits)} chunks')
    document = splits[2]
    print(document.page_content)
    print(document.metadata)
    
    #Creating the Chroma DB
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
        print("Deleted current database")

    #Create a new DB from the documents
    batch_size = 166  # Set to the maximum allowed batch size
    for i in range(0, len(splits), batch_size):
        batch = splits[i:i + batch_size]
        vectorstore = Chroma.from_documents(batch, embedding=embeddings, persist_directory=CHROMA_PATH)
    
    vectorstore.persist()
    
    print("Documents vectorized and saved in the chroma database")

