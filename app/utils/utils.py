import os
import logging
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_groq.chat_models import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()


os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')
os.environ['PINECONE_API_KEY']=os.getenv('PINECORN_API_KEY')
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ["GOOGLE_API_KEY"]=os.getenv('GOOGLE_API_KEY')
os.environ["GOOGLE_PROJECT_ID"]=os.getenv('GOOGLE_PROJECT_ID')


llm_model="llama-3.1-70b-versatile"
embedding_model="models/text-embedding-004"
vector_store_index_name="manifesto"
search_k=10
temp_dir="/temp"


embeddings=GoogleGenerativeAIEmbeddings(model=embedding_model)

retriever=PineconeVectorStore(embedding=embeddings, index_name=vector_store_index_name).as_retriever(search_kwargs={"k": search_k})

llm=ChatGroq(model=llm_model,
            temperature=0.5,
            max_tokens=None,
            timeout=None)


def load_pdf(path):
    manifesto_data=PyPDFLoader(path).load()
    return manifesto_data

def load_txt(path):
    manifesto_data=TextLoader(path).load()
    return manifesto_data

def split(docs):
    doc_splits = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=390,
        length_function=len,
        is_separator_regex=False,
    ).split_documents(docs)

    return doc_splits

def store(doc_splits, index_name=vector_store_index_name):
    pinecone_vectore_store=PineconeVectorStore.from_documents(documents=doc_splits, embedding=embeddings, index_name=index_name)
    return pinecone_vectore_store


def load_into_vector_store(directory=temp_dir):
    try:
        list_of_dirs=os.listdir(directory)
    
        for dir in list_of_dirs:
            relative_path=os.path.join(directory, dir)
            if os.path.splitext(dir)[1] == 'pdf':
                store(split(load_pdf(relative_path)))
            elif os.path.splitext(dir)[1] == 'txt':
                store(split(load_txt(relative_path)))
    except Exception as e:
        logging.exception(e)
            
            
            
def save_pdf_txt_on_temp_dir(uploaded_file, temp_file_path=temp_dir):
    try:
        file_path=os.path.join(temp_file_path, uploaded_file.name)
        with open(file_path, 'wb') as file_to_write:
            file_to_write.write(uploaded_file.read())
    except Exception as e:
        logging.exception(e)
            

