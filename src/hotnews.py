import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

BASE_URL = "https://hotnews.ro/ultima-ora"
SITE = "HotNews"

def download_list_page():
    response = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text

def parse_articles(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    today = datetime.now().date()

    articles = soup.select("article.ultima-ora")

    for article in articles:
        time_tag = article.select_one("time.entry-date")
        if not time_tag:
            continue

        published_iso = time_tag.get("datetime")
        if not published_iso:
            continue

        published_dt = datetime.fromisoformat(published_iso.replace("Z", "+00:00"))
        if published_dt.date() != today:
            continue

        title_tag = article.select_one("h2.entry-title a")
        title = title_tag.get_text(strip=True) if title_tag else None
        link = title_tag.get("href") if title_tag else None

        cat_tag = article.select_one(".hn-category-tag a")
        category = cat_tag.get_text(strip=True) if cat_tag else None

        excerpt_tag = article.select_one("a.excerpt")
        description = excerpt_tag.get_text(strip=True) if excerpt_tag else None

        results.append({
            "source": "HotNews",
            "title": title,
            "url": link,
            "category": category,
            "published_at": published_dt.strftime("%d/%m/%y %H:%M"),
            "description": description
        })

    return results