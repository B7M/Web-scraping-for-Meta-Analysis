import requests
import csv
import re
import time
import pandas as pd
from bs4 import BeautifulSoup

print("Please make sure your search URL from PubMed is including the papers with abstracts only.")
URL_input = input("Please paste search URL and press Enter:")
URL_ori = URL_input
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
})

outfile = open("scrapped.csv","w",newline='',encoding='utf-8')
writer = csv.writer(outfile)
df = pd.DataFrame(columns=['Title','Links'])

for i in range(10):
    page_num = i + 1
    URL_edit = URL_ori+"&page=" + str(page_num)   
    page = requests.get(URL_edit, headers=headers, timeout=None)
    soup = BeautifulSoup(page.content, "html.parser")
    time.sleep(1)

    results = soup.find("section", class_="search-results-list")

    job_elements = results.find_all("article", class_="full-docsum")
    for job_element in job_elements:
        links = job_element.find("a",class_="docsum-title")
        link_url = "https://pubmed.ncbi.nlm.nih.gov"+links["href"]
        title_element = links.text.strip()

        df2 = pd.DataFrame([[title_element, link_url]], columns=['Title','Links'])
        df = pd.concat([df, df2], ignore_index=True)

df.index += 1
df.to_csv('scrapped.csv',encoding='utf-8')
outfile.close()

print("Search completed!")

