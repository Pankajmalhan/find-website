from dotenv import load_dotenv
import os
import time

from utils.common import save_extracted_info

# Load environment variables from .env file
load_dotenv()
import requests
from utils.scrape_website import get_website_html_headless, get_website_text, check_about_page
from utils.summary import summarize_stuff_chain, summarize_map_reduce
from utils.keyword_extractor import get_keywords_and_title_from_text, get_title
from langchain_core.documents import Document
from tqdm import tqdm

def runner():
    start_time = time.time()
    WEBSITE_URL = "https://tftus.com"
    website_text = ""
    
    print("Fetching main website content...")
    content = get_website_text(WEBSITE_URL)
    if content is None:
        print("No website found")
        return
    else:
        print("Website text found")
        website_text = content

    print("Checking for 'About Us' page...")
    about_us_url = check_about_page(WEBSITE_URL)
    if about_us_url is not None:
        print(f"Fetching 'About Us' content from: {about_us_url}")
        about_us_content = get_website_text(about_us_url)
        if about_us_content is None:
            print("No content found for about us url")
        else:
            print("Content found for about us url")
            website_text += "\n\n" + about_us_content
    else:
        print("No 'About Us' link found")

    print("Summarizing content...")
    docs = [Document(page_content=content[i:i + 2000]) for i in tqdm(range(0, len(content), 2000), desc="Processing Content")]
    summarized_text = summarize_map_reduce(docs)
#     print(summarized_text)

    print("### Extracting the keywords and title")
    keywords_title = get_keywords_and_title_from_text(summarized_text)
    
    keywords = []
    title = ""

    # Check if keywords_title is not None before accessing its attributes
    if keywords_title:
       keywords = keywords_title.keywords if keywords_title.keywords is not None else []
       title = keywords_title.title if keywords_title.title is not None else ""

    print("### Saving extracted info to file")
    save_extracted_info(WEBSITE_URL, summarized_text, ",".join(keywords), title)

    total_time = time.time() - start_time
    print(f"Total time taken: {total_time} seconds")

if __name__ == "__main__":
    runner()