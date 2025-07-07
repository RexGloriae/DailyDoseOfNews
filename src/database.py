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
            url TEXT UNIQUE,
            published_at TEXT,
            content TEXT,
            author TEXT
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
