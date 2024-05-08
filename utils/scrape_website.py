import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

def get_website_text(url):    
    try:
        # Send a GET request to the URL
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove less meaningful HTML elements
            elements_to_remove = ["script", "style", "header", "footer","modal", "nav", "a", "head", "img", "noscript"]
            for tag in soup(elements_to_remove):
                tag.decompose()

            # Further clean up: removing menu items and advertisements if identified by class or id
            for tag in soup.find_all(['div', 'section']):
                if 'menu' in tag.get('class', '') or 'ad' in tag.get('id', ''):
                    tag.decompose()

            # Remove elements with CSS property 'display: none' or 'visibility: hidden' or 'opacity: 0'
            for tag in soup.find_all(style=True):
                style = tag['style'].replace(' ', '').lower()
                if 'display:none' in style or 'visibility:hidden' in style or 'opacity:0' in style:
                    tag.decompose()

             # Remove divs with class 'modal'
            for modal_div in soup.find_all('div', class_='modal'):
                modal_div.decompose()

            # Remove elements with classes or ids that suggest they are hidden
            hidden_indicators = ['hidden', 'hide', 'invisible', 'visuallyhidden']
            for tag in soup.find_all(True, class_=hidden_indicators):
                tag.decompose()
            for tag in soup.find_all(True, id=hidden_indicators):
                tag.decompose()


            # Extract text from the parsed HTML and normalize whitespace
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text).strip()  # Replaces multiple spaces with a single space, trims leading/trailing whitespace
            
            return text
        else:
            # Print an error message if the request was not successful
            print(f"Failed to fetch content from {url}, Status code: {response.status_code}")
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
    finally:
        driver.quit()

def get_website_html_headless(url):
    loader = AsyncChromiumLoader([url])
    html2text = Html2TextTransformer()
    html = loader.load()
    print(html)
    if html is None:
        return None
    documents = html2text.transform_documents(html)
    return documents

def is_about_page(url, content):
    """Check if the page content suggests it's an about page."""
    keywords = ['about us', 'who we are', 'our story', 'company info', 'our team', 'mission', 'vision', 'values', 'history']
    content = content.lower()
    matches = sum(content.count(keyword) for keyword in keywords)
    return matches > 2  # If there are more than two keyword matches, likely an about page.

def check_about_page(base_url):
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Define potential keywords to look for in link text
        about_pattern = re.compile(r'about|our story|who we are|company info|our team', re.IGNORECASE)

        candidate_links = []
        for link in soup.find_all('a', href=True):
            link_text = link.text.strip().lower()
            link_title = link.get('title', '').lower()

            # Check if the text or title of the anchor contains about keywords
            if about_pattern.search(link_text) or about_pattern.search(link_title):
                href = urljoin(base_url, link['href'])
                candidate_links.append(href)

        # Validate candidates
        for candidate in candidate_links:
            try:
                resp = requests.get(candidate, headers=headers, timeout=10)
                resp.raise_for_status()
                if is_about_page(candidate, resp.text):
                    return candidate
            except requests.exceptions.RequestException:
                continue

        return None
    except requests.exceptions.RequestException as e:
        return str(e)