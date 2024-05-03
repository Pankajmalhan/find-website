import re
import os

def save_extracted_info(website_url, summary, keywords):
       # Create filename from URL
    filename = re.sub(r'[^\w\-_\. ]', '_', website_url) + '.txt'
    full_filename = os.path.join("scraper_result", filename)
    print(full_filename)
    with open(full_filename, 'w') as file:
        file.write("Summarized Text:\n")
        file.write(summary + "\n\n")
        file.write("Keywords:\n")
        file.write(keywords + "\n")

    print(f"Output written to {filename}")