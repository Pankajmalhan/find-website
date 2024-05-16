from pymongo import MongoClient
import os
from dotenv import load_dotenv

MONGODB_ATLAS_CLUSTER_URI = os.environ.get("MONGODB_ATLAS_CLUSTER_URI")
DB_NAME = "accesfind"
COLLECTION_NAME = "websites"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

def get_website_collection():
       # initialize MongoDB python client
       client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
       MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
       return MONGODB_COLLECTION

def get_websites(skip=0, limit=20):
       collection =  get_website_collection();
       websites = collection.find({}).skip(skip).limit(limit)
       return websites

def is_website_exists(domain):
       collection =  get_website_collection();
       websiteCount = collection.count_documents({ 'domain' : domain})
       return websiteCount > 0

def insert_website(websiteObj):
       collection =  get_website_collection();
       response  = collection.insert_one(websiteObj)
       return response.inserted_id

def update_website(query, websiteObj):
       collection =  get_website_collection();
       response  = collection.update_one(query, {"$set":websiteObj})
       return response.upserted_id


def search_websites(embedding, limit=10, skip=0):
       collection =  get_website_collection();
       websites = collection.aggregate([
              {
                     "$vectorSearch": {
                            "index": ATLAS_VECTOR_SEARCH_INDEX_NAME,
                            "queryVector": embedding,
                            "numCandidates":100,
                            "path": "summary",
                            "limit": limit,
                     }
              },
              {
              "$project": {
                     "summary_text": 1,
                     "domain":1,
                     "title": 1,
                     "keywords": 1,
                     "updated_at": 1,
                     "summary": 1,
                     "score": { "$meta": "vectorSearchScore" }
              }
              }
       ])
       return websites