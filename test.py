import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from html import unescape

# Step 1: URL
url = "https://kagoz.com/business/century-group"

# Step 2: Send request
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


def decode_cfemail(cfemail_data):
    """Decode Cloudflare protected email"""
    # Extract the encoded string
    encoded = cfemail_data
    
    # First character is the XOR key
    key = int(encoded[:2], 16)
    
    # Decode the rest (each 2 chars is a hex byte)
    decoded = ''
    for i in range(2, len(encoded), 2):
        byte = int(encoded[i:i+2], 16)
        decoded_char = chr(byte ^ key)
        decoded += decoded_char
    
    return decoded

email_link = soup.find("div", id="contact").find_all("a", href=True)
email = "N/A"

for a in email_link:
    email_span = a.find("span", class_="__cf_email__")
    
    if email_span:
        cfemail_data = email_span.get('data-cfemail')
        if cfemail_data:
            email = decode_cfemail(cfemail_data)
            print(email)  # Will print the actual email
        else:
            # Fallback to text content
            email = email_span.text
            print(email)




