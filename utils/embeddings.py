from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer, util

def get_embeddings_gemini(text):
       embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
       vector = embeddings.embed_query(text)
       return vector

def get_embeddings_openai(text):
       embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
       vector = embeddings.embed_query(text)
       return vector

def get_embeddings_huggingface(text):
       # embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
       embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/bert-base-nli-mean-tokens")
       query_result = embeddings.embed_query(text)
       return query_result