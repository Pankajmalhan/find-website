from dotenv import load_dotenv
import os
load_dotenv()

import streamlit as st
from db_store.mongo import search_websites
from utils.embeddings import get_embeddings_huggingface
# MongoDB connection details
MONGO_URI = 'your_mongodb_uri'
DB_NAME = 'your_database_name'
COLLECTION_NAME = 'your_collection_name'


# Function to perform similarity search
def perform_similarity_search(query):
    # Assume that the collection has precomputed embeddings stored
    query_embedding = get_embeddings_huggingface([query])
    
    # Compute cosine similarity
    docs = search_websites(query_embedding[0].tolist())
    return docs

# Streamlit UI
st.title('Website Similarity Search')

# Input form for user query
query = st.text_input('Enter your query')

# Perform search if query is provided
if query:
    results = perform_similarity_search(query)
    
    st.write(f"Showing results for: {query}")
    print(results)
    
    for result in results:
        
        st.markdown(f"### Title: {result['title']}")
        st.markdown(f"**Domain:** {result['domain']}")
        st.markdown(f"**Description:** {result['summary_text'][0:100]}")
        st.markdown(f"**Score:** {result['score']}")
        st.markdown(f"**Keywords:** {', '.join(result['keywords'])}")
        st.markdown("---")

# Clear button
if st.button('Clear'):
    st.experimental_rerun()
