from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from llm_and_route_query import llm
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"]

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def load_FAISS_index(faiss_name):
    vectors = FAISS.load_local("faiss_index", embeddings, faiss_name, allow_dangerous_deserialization=True)
    return vectors

def get_context(index_path, question, sample_prompt, chat_history):
    vectors = load_FAISS_index(index_path)
    document_chain=create_stuff_documents_chain(llm,sample_prompt)
    retriever=vectors.as_retriever(search_kwargs={"k": 5})

    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    response=retrieval_chain.invoke({'input':question, "chat_history": chat_history})
    return response
