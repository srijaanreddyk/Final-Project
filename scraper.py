import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
import csv
import os
def get_internal_links(base_url,soup):
    base_domain=urlparse(base_url).netloc
    internal_links=set()
    for a_tag in soup.find_all('a',href=True):
        href=a_tag['href']
        joined_url=urljoin(base_url,href)
        parsed_url=urlparse(joined_url)
        if parsed_url.netloc==base_domain:
            cleaned_url=parsed_url.scheme +"://"+parsed_url.netloc+parsed_url.path
            internal_links.add(cleaned_url)
    return list(internal_links)
def scrape_page(url):
    try:
        headers={"User-Agent":"Mozilla/5.0"}
        res=requests.get(url,headers=headers,timeout=10)
        res.raise_for_status()
        soup=BeautifulSoup(res.text,'html.parser')
        title=soup.title.string.strip() if soup.title else "No Title"
        paragraphs=soup.find_all('p')
        text=''.join(p.get_text(strip=True)for p in paragraphs)
        return{"url":url,"title":title,"text":text}
    except Exception as e:
         return {"url": url, "title": "Error", "text": str(e)}
def scrape_with_subpages(main_url,max_pages=10):
    visited=set()
    scraped_data=[]
    headers={"User-Agent":"Mozilla/5.0"}
    res=requests.get(main_url,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    urls_to_scrape=[main_url]+get_internal_links(main_url,soup)
    urls_to_scrape=urls_to_scrape[:max_pages]
    for url in urls_to_scrape:
        if url not in visited:
            visited.add(url)
            result=scrape_page(url)
            scraped_data.append(result)
    return scraped_data
def save_to_csv(data,filename="scraped_data/scrapes_output.csv"):
    os.makedirs("scraped_data",exist_ok=True)
    with open(filename,mode='w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=["url","title","text"])
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    return filename