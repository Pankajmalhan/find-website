import pandas as pd
import requests
from utils.common import is_valid_url
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def process_websites(input_csv, output_file):
    """Process websites from a CSV file and write existing URLs to another file."""
    # Read the CSV file into a DataFrame
    data = pd.read_csv(input_csv)
    data =  data.loc[1500:3000]

        # Function to process each URL
    def process_url(url):
       try:
              if is_valid_url(url):
                     return url
              else:
                     return None
       except:
              print(f"Invalid URL: {url}")
              return None

        # Create a thread pool and process URLs in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Use list comprehension to create tasks for each URL and progress bar with tqdm
        results = list(tqdm(executor.map(process_url, data['url']), total=len(data['url']), desc="Processing URLs"))


    # Write the valid URLs to a file
    with open(output_file, 'a') as f:
        for result in results:
            if result:
                f.write(result + '\n')


