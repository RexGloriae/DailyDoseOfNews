from bs4 import BeautifulSoup
from datetime import datetime
from parser import download_site, conv_relative_date
from urllib.parse import urljoin

class EuroNews:
    def __init__(self):
        self.SITE = "EuroNews"
        self.URL = "https://www.euronews.ro/ultimele-stiri"

    def load_list(self):
        self.html = download_site(self.URL)

    def parse_articles(self):
        soup = BeautifulSoup(self.html, "html.parser")
        results = []
    
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
    
            results.append({
                "source": self.SITE,
                "title": title,
                "url": link,
                "published_at": published_str,
                "content": content
            })
    
        return results



if __name__ == "__main__":
    channel = EuroNews()
    channel.load_list()
    articles = channel.parse_articles()
    for art in articles:
        print(art)