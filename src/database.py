import sqlite3
from llm import get_description

class Database:
    def __init__(self):
        self.db_name = "news.db"
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            author TEXT,
            url TEXT UNIQUE,
            category TEXT,
            published_at TEXT,
            content TEXT,
            description TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save(self, article):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO articles (source, title, author, url, category, published_at, content, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get('source'),
                article.get('title'),
                article.get('author'),
                article.get('url'),
                article.get('category'),
                article.get('published_at'),
                article.get('content'),
                article.get('description')
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"[INFO] Article already exists in DB: {article['url']}")
        finally:
            conn.close()

    def get_all_articles(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM articles')
        rows = c.fetchall()
        conn.close()
        articles = [dict(row) for row in rows]
        return articles
    
    def article_exists(self, url):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT 1 FROM articles WHERE url = ?", (url,))
        exists = c.fetchone() is not None
        conn.close()
        return exists
    
    def fill_missing_descriptions(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()

        c.execute("SELECT id, url, content FROM articles WHERE description IS NULL")
        rows = c.fetchall()

        print(f"[INFO] Found {len(rows)} articles missing description...")

        for row in rows:
            article_id, url, content = row
            print(f"[LLM] Getting AI description from URL: {url}...")

            try:
                description = get_description(url)
                if description:
                    # 2. Update row
                    c.execute(
                        "UPDATE articles SET description = ? WHERE id = ?",
                        (description, article_id)
                    )
                    conn.commit()
                    print(f"[SUCCESS] Updated description for: {url}...")
                else:
                    print(f"[WARNING] No description generated for: {url}...")

            except Exception as e:
                print(f"[ERROR] Failed to generate description for {url}: {e}...")

        conn.close()