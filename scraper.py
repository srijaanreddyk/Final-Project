import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import io

def is_valid_subpage(link, base_domain):
    parsed = urlparse(link)
    return parsed.netloc == "" or base_domain in parsed.netloc

def get_internal_links(base_url, max_links=10):
    visited = set()
    to_visit = [base_url]
    domain = urlparse(base_url).netloc
    internal_links = []

    while to_visit and len(internal_links) < max_links:
        url = to_visit.pop()
        if url in visited:
            continue
        visited.add(url)
        try:
            res = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, 'html.parser')
            internal_links.append(url)

            for tag in soup.find_all('a', href=True):
                href = tag['href']
                full_link = urljoin(url, href)
                if is_valid_subpage(full_link, domain) and full_link not in visited:
                    to_visit.append(full_link)

        except Exception:
            continue

    return internal_links

def scrape_content_only(base_url, max_pages=10):
    links = get_internal_links(base_url, max_links=max_pages)
    content_list = []

    for link in links:
        try:
            res = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, 'html.parser')

            # Try to extract only <p> tags
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 30]

            content_text = "\n\n".join(paragraphs)
            content_list.append({"url": link, "content": content_text})
        except Exception:
            continue

    return content_list

def save_to_txt(data):
    lines = []
    for item in data:
        lines.append(f"URL: {item['url']}")
        lines.append(item['content'])
        lines.append("\n" + "-"*50 + "\n")
    return "\n".join(lines)

def save_to_csv(data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["URL", "Content"])
    for item in data:
        writer.writerow([item["url"], item["content"]])
    return output.getvalue()
