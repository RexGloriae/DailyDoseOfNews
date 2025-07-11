from pywebio.output import *
from pywebio.input import *
from pywebio.session import set_env
from pywebio import start_server
import requests
import time
from datetime import datetime
from logs import *

API_URL = "http://localhost:5000/articles"

class NewsApp:
    def __init__(self):
        self.articles = None
        self.selected_day = None
        self.days = None
        self.all = True
        self.load_all_articles()
        start_server(self.news_app, port=8080, debug=True)

    def load_all_articles(self):
        self.all = True
        self.articles = requests.get(API_URL).json()

    def load_articles_by_keyword(self, keyword):
        self.all = False
        self.articles = requests.get(f"{API_URL}/search", params={'q': keyword}).json()       

    def load_favorite_articles(self):
        self.all = False
        self.articles = requests.get(f"{API_URL}/favorites").json()

    def load_articles_from(self, source):
        self.all = False
        self.articles = requests.get(f"{API_URL}/source/{source}").json()

    def news_app(self):
        clear()
        set_env(title="📰 Daily Dose of News")
        put_markdown("# 📰 Daily Dose of News")
        self.buttons_panel()
        self.articles_panel()

    def buttons_panel(self):
        put_column([
            put_scope('top_controls'),
            put_scope('day_selector')
        ])

        with use_scope('top_controls', clear=True):
            put_markdown('### ⚙️ Controls')
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

        put_markdown('---')
        
        with use_scope('day_selector', clear=True):
            put_markdown('### 🗓️ Calendar')
            put_buttons([
                {"label": "🗓️ Pick a Day", "value": "pick_day"}
            ], onclick=self.handle_buttons)

    def articles_panel(self):
        try:
            articles_by_day = self.group_articles_by_day(self.articles)
            if not articles_by_day:
                put_info("There are no available articles!")
                logging.info("No available articles were found...")
                return

            self.days = sorted(articles_by_day.keys(), reverse=True)

            if self.selected_day is not None:
                day_articles = articles_by_day.get(self.selected_day, [])
                if not day_articles:
                    put_info(f"There are no articles available for {self.selected_day}!")
                    logging.info(f"No available articles found for {self.selected_day}...")
                    return
                
                self.print_day_articles(day_articles)
            else:
                if self.all is True:
                    self.show_placeholder()
                else:
                    self.print_all_articles(self.articles)

        except Exception as e:
            put_error(f"Error loading articles: {e}")
            logging.error(f"{e}")
    
    def print_all_articles(self, all_articles):
        articles = self.group_articles_by_day(all_articles)
        if not articles:
                put_info("There are no available articles!")
                logging.info("No available articles were found...")
                return
        for day, day_article in articles.items():
            with put_collapse(f"🗓️ News for {day}", open=False):
                for art in day_article:
                    status = ""
                    if art['read'] == 1:
                        status += "✅ Read  "
                    if art['favorite'] == 1:
                        status += "⭐ Favorite"

                    put_markdown(f"## {art['title']}")
                    put_markdown(f"### {status}")
                    put_text(f"Sursa: {art['source']} | Autor: {art.get('author', 'N/A')} | Publicat la: {art['published_at']}")
                    put_text(art.get('description') or "Fără descriere")
                    put_link("Citește mai mult", url=art['url'], new_window=True)
                    put_text("\n")

                    if art['read'] == 1:
                        put_buttons([
                            {'label': '❌ Mark as not Read', 'value': f"unread_{art['id']}"},
                        ], onclick=self.handle_buttons)
                    else:
                        put_buttons([
                            {'label': '✅ Mark as Read', 'value': f"read_{art['id']}"},
                        ], onclick=self.handle_buttons)
                    if art['favorite'] == 1:
                        put_buttons([
                            {'label': '💔 Remove from Favorite', 'value': f"unfav_{art['id']}"}
                        ], onclick=self.handle_buttons)
                    else:
                        put_buttons([
                            {'label': '⭐ Add Favorite', 'value': f"fav_{art['id']}"}
                        ], onclick=self.handle_buttons)

                    put_markdown("---")

    def print_day_articles(self, day_articles):
        with put_collapse(f"🗓️ News for {self.selected_day}", open=True):
            for article in day_articles:
                status = ""
                if article['read'] == 1:
                    status += "✅ Read  "
                if article['favorite'] == 1:
                    status += "⭐ Favorite"

                put_markdown(f"## {article['title']}")
                put_markdown(f"### {status}")
                put_text(f"Sursa: {article['source']} | Autor: {article.get('author', 'N/A')} | Publicat la: {article['published_at']}")
                put_text(article.get('description') or "Fără descriere")
                put_link("Citește mai mult", url=article['url'], new_window=True)
                put_text("\n")

                if article['read'] == 1:
                    put_buttons([
                        {'label': '❌ Mark as not Read', 'value': f"unread_{article['id']}"},
                    ], onclick=self.handle_buttons)
                else:
                    put_buttons([
                        {'label': '✅ Mark as Read', 'value': f"read_{article['id']}"},
                    ], onclick=self.handle_buttons)
                if article['favorite'] == 1:
                    put_buttons([
                        {'label': '💔 Remove from Favorite', 'value': f"unfav_{article['id']}"}
                    ], onclick=self.handle_buttons)
                else:
                    put_buttons([
                        {'label': '⭐ Add Favorite', 'value': f"fav_{article['id']}"}
                    ], onclick=self.handle_buttons)

                put_markdown("---")

    def group_articles_by_day(self, articles):
        articles_by_day = {}

        for art in articles:
            dt = datetime.strptime(art['published_at'], "%d/%m/%y %H:%M")
            day_key = dt.strftime("%d/%m/%y")

            if day_key not in articles_by_day:
                articles_by_day[day_key] = []

            art['_datetime_obj'] = dt
            articles_by_day[day_key].append(art)

        sorted_days = sorted(
            articles_by_day.keys(),
            key=lambda d: datetime.strptime(d, "%d/%m/%y"),
            reverse=True
        )

        for day in articles_by_day:
            articles_by_day[day].sort(key=lambda a: a['_datetime_obj'], reverse=True)

        for day in articles_by_day:
            for art in articles_by_day[day]:
                del art['_datetime_obj']

        return {day: articles_by_day[day] for day in sorted_days}


    def load_articles(self):
        put_info("Loading articles...")
        try:
            resp = requests.post(f"{API_URL}/load")
            put_success(resp.json().get("message"))
            time.sleep(3)
            self.load_all_articles()
            self.refresh_ui()
        except Exception as e:
            put_error(f"Loading error: {e}")
            logging.error(f"{e}")

    def fill_descriptions(self):
        put_info("Filling missing descriptions...")
        try:
            resp = requests.post(f"{API_URL}/fill_descriptions")
            put_success(resp.json().get("message"))
            time.sleep(3)
            self.refresh_ui()
        except Exception as e:
            put_error(f"Fill descriptions error: {e}")
            logging.error(f"{e}")

    def delete_articles(self):
        try:
            articles = requests.get(API_URL).json()
            articles_by_day = self.group_articles_by_day(articles)
            days = list(articles_by_day.keys())
            if not days:
                put_warning("There are no days to delete.")
                return

            day_to_delete = select("Select which day to delete:", days)
            if day_to_delete:
                resp = requests.delete(f"{API_URL}/by_date", json={"date": day_to_delete})
                put_success(resp.json().get("message"))
                self.load_all_articles()
                self.refresh_ui()
        except Exception as e:
            put_error(f"Delete error: {e}")
            logging.error(f"{e}")

    def handle_buttons(self, btn_val):
        self.selected_day = None
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
        elif btn_val.startswith('unread_'):
            self.unmark_read(int(btn_val.split('_')[1]))
        elif btn_val.startswith('unfav_'):
            self.unmark_favorite(int(btn_val.split('_')[1]))
        elif btn_val == "search":
            self.search()
        elif btn_val == "refresh":
            self.load_all_articles()
            self.refresh_ui()
        elif btn_val == "fav":
            self.show_favorites()
        elif btn_val == "filter":
            self.filter()
        elif btn_val == "stats":
            self.show_stats()
        elif btn_val == "pick_day":
            self.select_a_day()
    
    def select_a_day(self):
        today = datetime.now().strftime("%d%m%y")

        if today in self.days:
            default_day = today
        else:
            default_day = self.days[0]

        self.selected_day = select(
            label="🗓️ Pick a day",
            options=self.days,
            value=default_day
        )

        self.refresh_ui()

    def filter(self):
        source = input("Enter source (EuroNews, HotNews, ProTV): ")
        if not source:
            return
        try:
            self.load_articles_from(source)
            self.refresh_ui()
        except Exception as e:
            put_error(f"Error while filtering: {e}...")
            logging.error(f"{e}")

    def show_stats(self):
        try:
            stats = requests.get(f"{API_URL}/stats").json()            
            put_markdown("## 📊 **Statistics**")
            put_text(f"Total articles: {stats['total']}")
            put_text(f"Total days: {len(stats['per_day'])}")
            put_markdown("### 🗂️ By Source:")
            for src, count in stats['per_source']:
                put_text(f"{src}: {count}")
            put_markdown("### 📅 By Day:")
            for day, count in stats['per_day']:
                put_text(f"{day}: {count}")
        except Exception as e:
            put_error(f"Error at loading statistics: {e}...")
            logging.error(f"{e}")
            

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

    def unmark_read(self, article_id):
        try:
            requests.post(f"{API_URL}/unmark_read/{article_id}")
            toast("❌ Marked as not read!", duration=2)
        except Exception as e:
            toast(f"❌ Error: {e}")

    def unmark_favorite(self, article_id):
        try:
            requests.post(f"{API_URL}/unfavorite/{article_id}")
            toast("💔 Removed from favorites!", duration=2)
        except Exception as e:
            toast(f"❌ Error: {e}")

    def search(self):
        q = input("Enter keyword to search: ")
        if not q:
            return
        try:
            self.load_articles_by_keyword(q)
            self.refresh_ui()
        except Exception as e:
            put_error(f"Error when searching: {e}")
            logging.error(f"{e}")

    def show_favorites(self):
        try:
            self.load_favorite_articles()
            self.refresh_ui()
        except Exception as e:
            put_error(f"Error loading favorite articles: {e}...")
            logging.error(f"{e}")

    def refresh_ui(self):
        clear()
        put_markdown("# 📰 Daily Dose of News")
        self.buttons_panel()
        self.articles_panel()

    def show_placeholder(self):
        put_html("""
        <div style="
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 400px; 
            border: 2px dashed #aaa; 
            border-radius: 12px; 
            background: linear-gradient(135deg, #f0f4ff, #d9e4ff);
            color: #555;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
            <div style="font-size: 48px; margin-bottom: 20px;">📰</div>
            <h3 style="margin-bottom: 12px;">Welcome to Daily Dose of News!</h3>
            <p style="font-size: 18px; max-width: 320px; text-align: center; margin-bottom: 24px;">
                Pick a day using the button above to see news articles.
            </p>
        </div>
        """)


def main():
    app = NewsApp()

if __name__ == "__main__":
    main()