from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from parser import download_site
from urllib.parse import urljoin
import re

def conv_relative_date(text):
    now = datetime.now()
    text = text.strip().lower()
    if "minute" in text:
        minutes = int(re.search(r"(\d+)", text).group(1))
        return now - timedelta(minutes=minutes)
    elif "ora" in text or "ore" in text:
        hours = int(re.search(r"(\d+)", text).group(1))
        return now - timedelta(hours=hours)
    else:
        return "expired"

class ProTV:
    def __init__(self):
        self.URL = "https://stirileprotv.ro/ultimele-stiri/"
        self.SITE = "ProTV"

    def load_list(self):
        self.html = download_site(self.URL)
    

    def parse_articles(self):
        soup = BeautifulSoup(self.html, "html.parser")
        articles = soup.select("article.grid.article")
        results = []

        for article in articles:
            title_tag = article.select_one(".article-title a")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            link = urljoin(self.URL, link)

            lead_tag = article.select_one(".article-lead")
            content = lead_tag.get_text(strip=True) if lead_tag else None

            date_tag = article.select_one(".article-date")
            raw_date = date_tag.get_text(strip=True) if date_tag else None
            if raw_date:
                published_dt = conv_relative_date(raw_date)
                if published_dt == "expired": continue
                published_str = published_dt.strftime("%d/%m/%y %H:%M")
            else:
                published_str = None

            results.append({
                "source": "ProTV",
                "title": title,
                "url": link,
                "published_at": published_str,
                "content": content,
            })

        return results


if __name__ == "__main__": 
    channel = ProTV()
    channel.load_list()
    articles = channel.parse_articles()

    for art in articles:
        print(art)