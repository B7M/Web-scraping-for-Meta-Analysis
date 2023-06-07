import requests
import csv
import re
import time
import pandas as pd
from bs4 import BeautifulSoup

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
page_num = 0
pattern = r"start="
replacement = "start="+str(page_num*10)
URL_edit = re.sub(pattern, replacement, URL_ori)
page = requests.get(URL_edit, headers=headers, timeout=None)
soup = BeautifulSoup(page.content, "html.parser")
search_results = soup.find_all("div", class_="gs_ab_mdw")[1].text

for i in range(10):
    page_num_up = page_num + i
    pattern = r"start="+str(page_num_up*10)
    replacement = "start="+str(page_num_up*10)
    URL_edit = re.sub(pattern, replacement, URL_edit)
    
    page = requests.get(URL_edit, headers=headers, timeout=None)
    soup = BeautifulSoup(page.content, "html.parser")
    time.sleep(5)

    results = soup.find("div", id="gs_res_ccl_mid")

    job_elements = results.find_all("div", class_="gs_ri")
    for job_element in job_elements:
        links = job_element.find("a") 
        link_url = links["href"]
        title_element = links.text.strip()

        df2 = pd.DataFrame([[title_element, link_url]], columns=['Title','Links'])
        df = pd.concat([df, df2], ignore_index=True)

df.index += 1
df.to_csv('scrapped.csv',encoding='utf-8')
outfile.close()

print("Search completed!")

