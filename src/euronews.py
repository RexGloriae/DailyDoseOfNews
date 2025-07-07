from bs4 import BeautifulSoup
from datetime import datetime
from parser import download_site, conv_relative_date
from urllib.parse import urljoin
from llm import get_description
from database import Database

class EuroNews:
    def __init__(self):
        self.SITE = "EuroNews"
        self.URL = "https://www.euronews.ro/ultimele-stiri"
        self.load_list()

    def load_list(self):
        self.html = download_site(self.URL)

    def get_author(self, article_html):
        soup = BeautifulSoup(article_html, "html.parser")
        author_a = soup.find('a', href=lambda h: h and h.startswith('/autor/'))
        author = author_a.text.strip() if author_a else None
        return author

    def fetch_articles(self):
        soup = BeautifulSoup(self.html, "html.parser")
    
        for li in soup.select('li.flex.flex-row'):
            raw_date_el = li.select_one('time')
            if raw_date_el:
                raw_date = raw_date_el.text.strip()
                parsed_date = conv_relative_date(raw_date)
                if not isinstance(parsed_date, datetime):
                    continue
                published_str = parsed_date.strftime("%d/%m/%y %H:%M")
            else:
                published_str = None
    
            a_title = li.select_one('h1 a')
            title = a_title.text.strip() if a_title else None
            link = urljoin(self.URL, a_title['href']) if a_title else None
    
            content_a = li.select_one('div.line-clamp-3 a')
            content = content_a.text.strip() if content_a else None

            category_span = li.find('span', class_=lambda c: c and 'text-neon-blue' in c)
            category = category_span.text.strip() if category_span else None

            print(f"[DOWNLOAD] Fetching article from URL: {link}...")
            article = download_site(link)
            author = self.get_author(article)

            print(f"[LLM] Getting AI description from URL: {link}...")
            description = get_description(link)
    
            result = {
                "source": self.SITE,
                "title": title,
                "author": author,
                "url": link,
                "category": category,
                "published_at":  published_str,
                "content": content,
                "description": description
                }
            
            print(f"[INFO] Saving article to database...")
            Database().save(result)