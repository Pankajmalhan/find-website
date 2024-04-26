import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_transformers import Html2TextTransformer

def get_website_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text from the parsed HTML
            text = soup.get_text()
            return text
        else:
            # Print an error message if the request was not successful
            print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"An error occurred: {e}")
        return None
    
def get_website_html(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the HTML content
            return response.content
        else:
            # Print an error message if the request was not successful
            print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request
        print(f"An error occurred: {e}")
        return None

def get_website_html_headless(url):
    loader = AsyncChromiumLoader([url])
    html2text = Html2TextTransformer()
    html = loader.load()
    if html is None:
        return None
    documents = html2text.transform_documents(html)
    return documents

    

