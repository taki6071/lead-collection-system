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


def scrap_detail_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    details = {}
    
    #1
    name = soup.find("div", id="home").find("span").text.strip()
    details['Name'] = name if name else "N/A"

    #2
    email_link = soup.find("div", id="contact").find_all("a", href=True)
    email = "N/A"

    for a in email_link:
        email_span = a.find("span", string=re.compile(r"@"))
        if email_span:
            email = email_span.text.strip()
            break

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
        address_span = li.find("span", string=re.compile(r"Bangladesh|Dhaka|Chittagong|Sylhet", re.IGNORECASE))
        if address_span:
            address = address_span.text.strip()
            break

    details['Address'] = address

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