import sqlite3

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
