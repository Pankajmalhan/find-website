import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_community.document_transformers import Html2TextTransformer

def get_website_text(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

             # Remove script and style elements
            elements_to_remove = ["script", "style", "header", "footer", "nav", "form", "a"]
            for script_or_style in soup(elements_to_remove):
                script_or_style.decompose()

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

def check_about_page(url):
       try:
        # Send a HTTP request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad requests (4XX or 5XX)

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for all anchor tags
        for link in soup.find_all('a'):
            # Check if the text of the anchor contains 'About' or 'About Us'
            if 'about' in link.text.strip().lower():
                # Return the href attribute of the anchor tag
                href = link.get('href')
                if href:
                    # Check if the link is absolute or relative
                    if href.startswith('http'):
                        return href
                    else:
                        # Construct the full URL if the link is relative
                        from urllib.parse import urljoin
                        return urljoin(url, href)

        return "No 'About Us' link found."
       except requests.exceptions.RequestException as e:
        return str(e)
    

