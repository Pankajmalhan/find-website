import re
import os
from urllib.parse import urlparse

def save_extracted_info(website_url, summary, keywords, title):
       # Create filename from URL
    filename = re.sub(r'[^\w\-_\. ]', '_', website_url) + '.txt'
    full_filename = os.path.join("scraper_result", filename)
    print(full_filename)
    with open(full_filename, 'w') as file:
        file.write("Summarized Text:\n")
        file.write(summary + "\n\n")
        file.write("Keywords:\n")
        file.write(keywords + "\n")
        file.write("Title:\n")
        file.write(title + "\n")

    print(f"Output written to {filename}")


def clean_text(text):
    cleaned_text = text.replace("\n\n", ' ')
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    return cleaned_text



def get_domain(url):
    # Parse the URL to extract the domain
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Remove port numbers if any
    domain = domain.split(':')[0]
    
    # Regular expression to remove 'www.' and '.com'
    clean_domain = re.sub(r'^(www\.)|(\.com)$', '', domain)
    return clean_domain