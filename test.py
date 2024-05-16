from dotenv import load_dotenv
import os
load_dotenv()

import time
import re
from utils.common import save_extracted_info, clean_text, get_domain, lowercase_list, is_valid_url
from db_store.mongo import update_website, is_website_exists,insert_website
# Load environment variables from .env file
import requests
from utils.scrape_website import get_website_html_headless, get_website_text, check_about_page
from utils.summary import summarize_stuff_chain, summarize_map_reduce
from utils.keyword_extractor import get_keywords_and_title_from_text, get_title
from utils.splitter import get_documents
from langchain_core.documents import Document
from tqdm import tqdm
from utils.embeddings import get_embeddings_huggingface, get_embeddings_gecko
import datetime

def runner():
    WEBSITE_URL = "https://www.llamaindex.ai"
    start_time = time.time()

    print(f"Start time: {datetime.datetime.now()}")
    print("Checking url exist or not")
    domain = get_domain(WEBSITE_URL)
    is_valid = is_valid_url(WEBSITE_URL)

    if not is_valid:
        print(f"Invalid URL: {WEBSITE_URL}")
        return
    website_text = ""

    print("Checking for 'About Us' page...")
    about_us_url = check_about_page(WEBSITE_URL)
    if about_us_url is not None:
        print(f"Fetching 'About Us' content from: {about_us_url}")
        about_us_content = get_website_text(about_us_url)
        if about_us_content:
            print("Content found for about us url")
            website_text = about_us_content.strip()
    else:
        print("No 'About Us' link found")

    if not website_text:
        print("Fetching main website content...")
        content = get_website_text(WEBSITE_URL)
        if content:
            content = content.strip()
            website_text = content

    if not website_text:
        print(f"No content found for {WEBSITE_URL}")
        return


    cleaned_text = clean_text(website_text)
    print(f'cleaned text size: {len(cleaned_text)}')

    docs = get_documents(cleaned_text)
    summarized_text = summarize_map_reduce(docs)

    if summarized_text is None or len(summarized_text.strip())==0:
        print("No summarized text found")
        return

    print("### Extracting the keywords and title")
    keywords_title = get_keywords_and_title_from_text(summarized_text)
    
    keywords = []
    title = ""

    # Check if keywords_title is not None before accessing its attributes
    if keywords_title:
       keywords = keywords_title.keywords if keywords_title.keywords is not None else []
       title = keywords_title.title if keywords_title.title is not None else ""

    print("###Getting text embeddings")
    embeddings_summarized_text = get_embeddings_huggingface([summarized_text])
    is_website_already_exists = is_website_exists(domain)

    now = datetime.datetime.now()
    formatted_date = now.strftime('%d/%m/%Y %H:%M')

    website_object = {
        "summary": embeddings_summarized_text[0].tolist(),
        "summary_text": summarized_text,
        "domain": domain,
        "title": title,
        "keywords":lowercase_list(keywords),
        "updated_at": formatted_date,
    } 
    if is_website_already_exists:
        print("Website already exists in the database, so updating")
        update_website({"domain":domain}, website_object)
    else:
        print("Website does not exist in the database, so inserting")
        insert_website(website_object)
        print(f"Inserted website: {domain}")



    total_time = time.time() - start_time
    print(f"Total time taken: {total_time} seconds")

if __name__ == "__main__":
    runner()