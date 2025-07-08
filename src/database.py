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
            description TEXT,
            read INTEGER DEFAULT 0,
            favorite INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def save(self, article):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO articles (source, title, author, url, category, published_at, content, description, read, favorite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
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
        print("[INFO] Trying to fill missing descripitons...")
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

    def delete_articles_by_date(self, day_str):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM articles WHERE published_at LIKE ?", (f"{day_str}%",))
        conn.commit()
        conn.close()

    def mark_as_read(self, art_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE articles SET read=1 WHERE id=?', (art_id,))
        conn.commit()
        conn.close()

    def mark_as_favorite(self, art_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('UPDATE articles SET favorite=1 WHERE id=?', (art_id,))
        conn.commit()
        conn.close()

    def get_favorites(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM articles WHERE favorites=1')
        rows = c.fetchall()
        conn.close()
        articles = [dict(row) for row in rows]
        return articles
    
    def get_by_src(self, src):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM articles WHERE source=?', (src,))
        rows = c.fetchall()
        conn.close()
        articles = [dict(row) for row in rows]
        return articles    
    def search_articles(self, keyword):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        like_kw = f"%{keyword}%"
        c.execute('''
            SELECT * FROM articles 
            WHERE title LIKE ? OR content LIKE ? OR description LIKE ?
        ''', (like_kw, like_kw, like_kw))
        rows = c.fetchall()
        conn.close()
        articles = [dict(row) for row in rows]
        return articles

    def get_stats(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM articles')
        total = c.fetchone()[0]
    
        c.execute('SELECT source, COUNT(*) FROM articles GROUP BY source')
        per_source = c.fetchall()
    
        c.execute('SELECT substr(published_at, 1, 8) AS day, COUNT(*) FROM articles GROUP BY day')
        per_day = c.fetchall()
    
        conn.close()
        return {
            "total": total,
            "per_source": per_source,
            "per_day": per_day
        }