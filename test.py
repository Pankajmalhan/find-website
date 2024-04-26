from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from utils.scrape_website import get_website_html_headless, get_website_text
from utils.summary import summarize_stuff_chain
from langchain_core.documents import Document

def runner():
       content= get_website_text("http://tftus.com")
       if content is None:
              print("No website found")
              return 0
       docs = [Document(page_content=content[i:i + 2000]) for i in range(0, len(content), 2000)]
       summarized_text= summarize_stuff_chain(docs)
       print(summarized_text)


if __name__ == "__main__":
       runner()