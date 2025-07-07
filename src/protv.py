from bs4 import BeautifulSoup
from parser import download_site, conv_relative_date
from urllib.parse import urljoin
from llm import get_description

class ProTV:
    def __init__(self):
        self.URL = "https://stirileprotv.ro/ultimele-stiri/"
        self.SITE = "ProTV"

    def load_list(self):
        self.html = download_site(self.URL)

    def get_category(self, art_html):
        soup = BeautifulSoup(art_html, "html.parser")
        cat_tag = soup.select_one('div.article--section-information a')
        cat = cat_tag.text.strip() if cat_tag else None
        return cat
    
    def get_author(self, art_html):
        soup = BeautifulSoup(art_html, "html.parser")
        auth_tag = soup.select_one('div.author--name a')
        auth = auth_tag.text.strip() if auth_tag else None
        return auth

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

            curr_art = download_site(link)
            author = self.get_author(curr_art)
            category = self.get_category(curr_art)

            description = get_description(link)

            results.append({
                "source": "ProTV",
                "title": title,
                "author": author,
                "url": link,
                "category": category,
                "published_at": published_str,
                "content": content,
                "description": description
            })

        return results


if __name__ == "__main__": 
    channel = ProTV()
    channel.load_list()
    articles = channel.parse_articles()

    for art in articles:
        print(art)