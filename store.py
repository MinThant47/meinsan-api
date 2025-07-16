from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"]

def vector_embedding(file_path, name):

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    loader = TextLoader(file_path, encoding='utf-8')
    docs=loader.load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200) ## Chunk Creation
    final_documents=text_splitter.split_documents(docs[:20]) #splitting
    vectors=FAISS.from_documents(final_documents,embeddings) #vector google embeddings
    index_path = "faiss_index" + name
    vectors.save_local("faiss_index",name)
    return vectors

# vectors = vector_embedding(r"files\YTUFAQ.txt","YTUFAQ")
# vectors1 = vector_embedding(r"files\YTUEC.txt","YTUEC")
# vectors2 = vector_embedding(r"files\YTUHostel.txt","YTUHostel")
# vectors3 = vector_embedding(r"files\YTUExam.txt","YTUExam")
# vectors4 = vector_embedding(r"files\YTUMajors.txt","YTUMajors")
# vectors5 = vector_embedding(r"files\YTUMap.txt","YTUMap")
