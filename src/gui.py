from pywebio.output import *
from pywebio.input import *
from pywebio import start_server
import requests
import time

API_URL = "http://localhost:5000/articles"

class NewsApp:
    def __init__(self):
        self.articles = None
        self.load_all_articles()
        start_server(self.news_app, port=8080, debug=True, title="Daily Dose of News")

    def load_all_articles(self):
        self.articles = requests.get(API_URL).json()

    def load_articles_by_keyword(self, keyword):
        self.articles = requests.get(f"{API_URL}/search", params={'q': keyword}).json()       

    def news_app(self):
        clear()
        put_markdown("# 📰 Daily Dose of News")
        self.buttons_panel()
        self.articles_panel()

    def buttons_panel(self):
        put_buttons([
            {"label": "📥 Load articles", "value": "load"},
            {"label": "📝 Fill Descriptions", "value": "fill"},
            {"label": "🔎 Search", "value": "search"},
            {"label": "🔄 Refresh", "value": "refresh"},
            {"label": "🗂️ Filter by Source", "value": "filter"},
            {"label": "⭐ Favorites", "value": "fav"},
            {"label": "📊 Stats", "value": "stats"},
            {"label": "🗑️ Delete Older Day", "value": "del"}
        ], onclick=self.handle_buttons)

    def articles_panel(self):
        try:
            articles_by_day = self.group_articles_by_day(self.articles)
            for day, day_articles in articles_by_day.items():
                with put_collapse(f"📅 {day}", open=False):
                    for article in day_articles:
                        put_markdown(f"### {article['title']}")
                        put_text(f"Sursa: {article['source']} | Autor: {article.get('author', 'N/A')} | Publicat la: {article['published_at']}")
                        put_text(article.get('description') or "Fără descriere")
                        put_link("Citește mai mult", url=article['url'], new_window=True)
                        put_text("\n")
                        put_buttons([
                            {'label': '✅ Mark as Read', 'value': f"read_{article['id']}"},
                            {'label': '⭐ Add Favorite', 'value': f"fav_{article['id']}"}
                        ], onclick=self.handle_buttons)
                        put_markdown("---")
        except Exception as e:
            put_error(f"Eroare la încărcarea știrilor: {e}")

    def group_articles_by_day(self, articles):
        articles_by_day = {}
        for art in articles:
            day = art['published_at'][:8]
            if day not in articles_by_day:
                articles_by_day[day] = []
            articles_by_day[day].append(art)

        sorted_days = sorted(articles_by_day.keys(), reverse=True)
        return {day: articles_by_day[day] for day in sorted_days}

    def load_articles(self):
        put_info("Loading articles...")
        try:
            resp = requests.post(f"{API_URL}/load")
            put_success(resp.json().get("message"))
            time.sleep(3)
            self.load_all_articles()
            self.news_app()
        except Exception as e:
            put_error(f"Loading error: {e}")

    def fill_descriptions(self):
        put_info("Filling missing descriptions...")
        try:
            resp = requests.post(f"{API_URL}/fill_descriptions")
            put_success(resp.json().get("message"))
            time.sleep(3)
            self.news_app()
        except Exception as e:
            put_error(f"Fill descriptions error: {e}")

    def delete_articles(self):
        try:
            articles = requests.get(API_URL).json()
            articles_by_day = self.group_articles_by_day(articles)
            days = list(articles_by_day.keys())
            if not days:
                put_warning("Nu există zile de șters.")
                return

            day_to_delete = select("Selectează ziua de șters:", days)
            if day_to_delete:
                resp = requests.delete(f"{API_URL}/by_date", json={"date": day_to_delete})
                put_success(resp.json().get("message"))
                self.load_all_articles()
                self.news_app()
        except Exception as e:
            put_error(f"Delete error: {e}")

    def handle_buttons(self, btn_val):
        if btn_val == "fill":
            self.fill_descriptions()
        elif btn_val == "del":
            self.delete_articles()
        elif btn_val == "load":
            self.load_articles()
        elif btn_val.startswith('read_'):
            self.mark_read(int(btn_val.split('_')[1]))
        elif btn_val.startswith('fav_'):
            self.mark_favorite(int(btn_val.split('_')[1]))
        elif btn_val == "search":
            self.search()
        elif btn_val == "refresh":
            self.load_all_articles()
            self.news_app()
        #elif btn_val == "fav":

        #elif btn_val == "filter":

        #elif btn_val == "stats":

    def mark_read(self, article_id):
        try:
            requests.post(f"{API_URL}/mark_read/{article_id}")
            toast("✅ Marked as read!", duration=2)
        except Exception as e:
            toast(f"❌ Error: {e}")

    def mark_favorite(self, article_id):
        try:
            requests.post(f"{API_URL}/favorite/{article_id}")
            toast("⭐ Added to favorites!", duration=2)
        except Exception as e:
            toast(f"❌ Error: {e}")

    def search(self):
        q = input("Enter keyword to search: ")
        if not q:
            return
        try:
            self.load_articles_by_keyword(q)
            self.news_app()
        except Exception as e:
            put_error(f"Eroare la cautare: {e}")

def main():
    app = NewsApp()

if __name__ == "__main__":
    main()