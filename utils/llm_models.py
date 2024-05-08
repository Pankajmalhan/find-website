
from langchain_community.chat_models import ChatOpenAI
import vertexai
from langchain_google_vertexai import VertexAI
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
from langchain_groq import ChatGroq
import os

set_llm_cache(SQLiteCache(database_path=".langchain.db"))


def gemini_model():
       location = "us-central1"
       project_id = "accessfind-7165sxdh4e"
       vertexai.init(project=project_id, location=location)
       # MODEL_ID="text-bison@001"
       MODEL_ID = "gemini-1.0-pro-002"
       llm = VertexAI(model_name=MODEL_ID)
       return llm

def groq_model():
       GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
       llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama3-8b-8192")
       return llm

def openai_model():
       llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
       return llm
