from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import csv

# ✅ Path to your downloaded ChromeDriver (use raw string to avoid backslash errors)
CHROMEDRIVER_PATH = r"C:\Users\ruthika\OneDrive\Documents\web-scrapper-final-project\chromedriver.exe"

# ✅ Set Chrome options
options = Options()
options.add_argument('--headless')  # comment this out if you want to see browser
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("user-agent=Mozilla/5.0")

# ✅ Initialize Chrome driver
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# ✅ Extract internal links
def get_internal_links(base_url, soup):
    base_domain = urlparse(base_url).netloc
    internal_links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == base_domain:
            internal_links.add(full_url)
    return list(internal_links)

# ✅ Scrape a single page and wait for JS content
def scrape_page(url):
    try:
        driver.get(url)

        # Wait until <p> tag is loaded (replace with a more specific tag if needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "p"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)

        return {"url": url, "title": title, "text": text}

    except Exception as e:
        return {"url": url, "title": "Error", "text": str(e)}

# ✅ Scrape main + subpages
def scrape_with_subpages(main_url, max_pages=10):
    visited = set()
    scraped_data = []

    try:
        driver.get(main_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = [main_url] + get_internal_links(main_url, soup)
        links = links[:max_pages]

        for url in links:
            if url not in visited:
                visited.add(url)
                scraped_data.append(scrape_page(url))

    except Exception as e:
        scraped_data.append({"url": main_url, "title": "Error", "text": str(e)})

    return scraped_data

# ✅ Save output to CSV
def save_to_csv(data, filename="scraped_data/scraped_output.csv"):
    os.makedirs("scraped_data", exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "title", "text"])
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    return filename
