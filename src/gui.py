from pywebio.output import *
from pywebio.input import *
from pywebio import start_server
import requests
import time

API_URL = "http://localhost:5000/articles"

class NewsApp:
    def __init__(self):
        start_server(self.news_app, port=8080, debug=True, title="Daily Dose of News")

    def news_app(self):
        clear()
        put_markdown("# 📰 Daily Dose of News")

        def buttons_panel():
            put_button("🔄 Refresh", onclick=self.refresh_articles, small=True)
            put_buttons([
                {"label": "📝 Fill Descriptions", "value": "fill"},
                {"label": "🗑️ Delete Older Day", "value": "delete"},
            ], onclick=self.handle_buttons)

        def articles_panel():
            try:
                articles = requests.get(API_URL).json()
                articles_by_day = self.group_articles_by_day(articles)

                for day, day_articles in articles_by_day.items():
                    with put_collapse(f"📅 {day}", open=False):
                        for article in day_articles:
                            put_markdown(f"### {article['title']}")
                            put_text(f"Sursa: {article['source']} | Autor: {article.get('author', 'N/A')} | Publicat la: {article['published_at']}")
                            put_text(article.get('description') or "Fără descriere")
                            put_link("Citește mai mult", url=article['url'], new_window=True)
                            put_markdown("---")

            except Exception as e:
                put_error(f"Eroare la încărcarea știrilor: {e}")

        put_row([
            put_column([buttons_panel()], size='100px'),
            put_column([articles_panel()])
        ])

    def group_articles_by_day(self, articles):
        articles_by_day = {}
        for art in articles:
            day = art['published_at'][:8]
            if day not in articles_by_day:
                articles_by_day[day] = []
            articles_by_day[day].append(art)

        sorted_days = sorted(articles_by_day.keys(), reverse=True)
        return {day: articles_by_day[day] for day in sorted_days}

    def refresh_articles(self):
        put_info("Refreshing articles...")
        try:
            resp = requests.post(f"{API_URL}/refresh")
            put_success(resp.json().get("message"))
            time.sleep(3)
            self.news_app()
        except Exception as e:
            put_error(f"Refresh error: {e}")

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
                self.news_app()
        except Exception as e:
            put_error(f"Delete error: {e}")

    def handle_buttons(self, btn_val):
        if btn_val == "fill":
            self.fill_descriptions()
        elif btn_val == "delete":
            self.delete_articles()

def main():
    app = NewsApp()

if __name__ == "__main__":
    main()
