from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer, util
from vertexai.preview.language_models import TextEmbeddingModel

def get_embeddings_gemini(text):
       embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
       vector = embeddings.embed_query(text)
       return vector

def get_embeddings_openai(text):
       embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
       vector = embeddings.embed_query(text)
       return vector

def get_embeddings_huggingface(sentences):
       model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
       embeddings = model.encode(sentences)
       return embeddings

def get_embeddings_gecko(text):
       model = TextEmbeddingModel.from_pretrained("textembedding-gecko")
       embeddings = model.get_embeddings([text])
       return embeddings[0].values