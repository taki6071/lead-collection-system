import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random


def scrap_category_list_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find("div", class_="pb-8").find_all("a", href=True)

    category_links = []

    for a in links:
        href = a['href']
        if '/categories/' in href:
            full_url = "https://kagoz.com" + href if href.startswith('/') else href
            category_links.append({
                'detail_url' : full_url
            })

    return category_links



def scrap_list_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=True)
    
    agency_links = []

    for li in links:
        href = li['href']

        if '/business/' in href:
            full_url = "https://kagoz.com" + href if href.startswith('/') else href
            agency_links.append({
                'detail_url' : full_url
            })


    return agency_links



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



def scrap_detail_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    details = {}
    
    #1
    name = soup.find("div", id="home").find("span").text.strip()
    details['Name'] = name if name else "N/A"

    #6
    cate = soup.find("div", id="home").find("div", class_=["text-color-white","text-left","font-inter","font-medium","text-lg"]).text.strip()
    details['Category'] = cate if cate else "N/A"

    #2
    email_link = soup.find("div", id="contact").find_all("a", href=True)
    email = "N/A"

    for a in email_link:
        email_span = a.find("span", class_="__cf_email__")
    
        if email_span:
            cfemail_data = email_span.get('data-cfemail')
            if cfemail_data:
                email = decode_cfemail(cfemail_data)
            else:
                email = email_span.text

    details['Email'] = email
    

    #3
    phone_tag = soup.find("div", id="contact").find_all("a", href=True)
    phone = "N/A"

    for link in phone_tag:
        phone_span = link.find("span", string=re.compile(r"\d{11}"))
        if phone_span:
            phone = phone_span.text.strip()
            break


    details['Phone'] = phone

    #4
    address_tag = soup.find("div", id="contact").find_all("a", href=True)
    address = "N/A"

    for li in address_tag:
        address_span = li.find("span", string=re.compile(r"^(?!http|https|www\.).*(Bangladesh|Dhaka|Chittagong|Sylhet)", re.IGNORECASE))
        if address_span:
            address = address_span.text.strip()
            break

    details['Address'] = address

    #7
    cities = sorted([
    "Bagerhat", "Bandarban","Brahmanbaria", "Chandpur", "Chittagong", "Comilla", "Cox's Bazar", "Dhaka", "Sunamganj", "Sylhet", "Tangail", "Thakurgaon"])

    parts = [p.strip() for p in address.split(',')]

    result = None
    for part in parts:
        for city in cities:
            if city in part:
                result = city
                break
        if result:
            break

    details['District'] = result if result else "N/A"

    #5
    web_tag = soup.find("div", id="contact").find_all("a", href=True)
    website = "N/A"

    for a in web_tag:
        web_span = a.find("span", string=re.compile(r"http://|https://", re.IGNORECASE))
        if web_span:
            website = web_span.text.strip()
            break

    details['Website'] = website


    return details


#start
category_list_url = "https://kagoz.com"
category = scrap_category_list_page(category_list_url)

all_category = []
for cat in category:
    agencies = scrap_list_page(cat['detail_url'])


    all_data = []
    for agency in agencies:
        details = scrap_detail_page(agency['detail_url'])

        all_data.append(details)

        time.sleep(random.uniform(0.5, 2.5))

    all_category.append(all_data)



df = pd.DataFrame(all_category)
df.to_csv("leads.csv", index=False)

print("Leads collected!")