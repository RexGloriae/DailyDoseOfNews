from bs4 import BeautifulSoup
from datetime import datetime
from parser import download_site
from llm import get_description
from database import Database
from logs import *

class HotNews:
    def __init__(self):
        self.URL = "https://hotnews.ro/ultima-ora"
        self.SITE = "HotNews"
        self.load_list()
    
    def load_list(self):
        self.html = download_site(self.URL)
    
    def get_author(self, article_html):
        soup = BeautifulSoup(article_html, "html.parser")
        author_a = soup.select_one('a[rel="author"]')
        author = author_a.text.strip() if author_a else None
        return author

    def fetch_articles(self):
        soup = BeautifulSoup(self.html, "html.parser")
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

            if Database().article_exists(link) is True:
                print(f"[INFO] The database already has the article with URL: {link} - skipping...")
                logging.info(f"Skipping article with url: {link}...")
                continue 

            cat_tag = article.select_one(".hn-category-tag a")
            category = cat_tag.get_text(strip=True) if cat_tag else None

            excerpt_tag = article.select_one("a.excerpt")
            content = excerpt_tag.get_text(strip=True) if excerpt_tag else None

            print(f"[DOWNLOAD] Fetching article from URL: {link}...")
            logging.info(f"Downloading article from {link}...")
            curr_art = download_site(link)
            author = self.get_author(curr_art)

            logging.info("Fetching AI description...")
            print(f"[LLM] Getting AI description from URL: {link}...")
            description = get_description(link)

            result = {
                "source": self.SITE,
                "title": title,
                "author": author,
                "url": link,
                "category": category,
                "published_at":  published_dt.strftime("%d/%m/%y %H:%M"),
                "content": content,
                "description": description
                }
            
            print(f"[INFO] Saving article to database...")
            logging.info("Saving article to database")
            Database().save(result)