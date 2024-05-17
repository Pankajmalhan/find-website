from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()

import time
import streamlit as st
from db_store.mongo import search_websites
from utils.embeddings import get_embeddings_huggingface


# MongoDB connection details
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

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
    start_time = time.time()  # Start timer
    
    results = perform_similarity_search(query)
    
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    
    st.write(f"Showing results for: {query}")
    st.write(f"Time taken: {elapsed_time:.2f} seconds")  # Display elapsed time
    
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
