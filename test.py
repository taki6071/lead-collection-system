import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: URL
url = "https://www.yellowpages.com/search?search_terms=real+estate&geo_location_terms=dhaka"

# Step 2: Send request
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)

print(response.text[:5000])