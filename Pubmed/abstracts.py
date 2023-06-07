import requests
import csv 
import pandas as pd
from bs4 import BeautifulSoup

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
})
outfile = open("abstracts.csv","w",newline='',encoding='utf-8')
writer = csv.writer(outfile)
df = pd.DataFrame(columns=['Title','Abstract','Link'])

with open('scrapped.csv', 'r') as file:
    file_reader = csv.reader(file)
    next(file_reader)
    for row in file_reader:
        URL_input = row[2]
        page = requests.get(URL_input, headers=headers, timeout=None)
        soup = BeautifulSoup(page.content, "html.parser")
        if soup.find("div", class_="abstract-content selected"):
            search_results = soup.find("div", class_="abstract-content selected").find('p')
            search_results=search_results.get_text(strip=True)
            df2 = pd.DataFrame([[row[1],search_results,row[2]]], columns=['Title','Abstract','Link'])
            df = pd.concat([df, df2], ignore_index=True)
        else:
            df2 = pd.DataFrame([[row[1],"No abstract available",row[2]]], columns=['Title','Abstract','Link'])
            df = pd.concat([df, df2], ignore_index=True)
df.to_csv('abstracts.csv',encoding='utf-8')
outfile.close()

print("Abstracts are scraped!")

