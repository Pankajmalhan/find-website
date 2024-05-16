import pandas as pd
from runner import runner
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def scrape_website():
    """Process websites from a CSV file and write existing URLs to another file."""
    # Read the CSV file into a DataFrame
    data = pd.read_csv("data/valid.websites.csv")
    START_INDEX = 0
    END_INDEX = 10
    data =  data.loc[START_INDEX:END_INDEX]


       # Create a thread pool and process URLs in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Use list comprehension to create tasks for each URL and progress bar with tqdm
        results = list(tqdm(executor.map(runner, data['url']), total=len(data['url']), desc="Scrapping Website"))

if __name__ == "__main__":
    scrape_website()




