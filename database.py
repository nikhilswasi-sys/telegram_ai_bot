import sqlite3
import hashlib

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id TEXT UNIQUE
)
""")
conn.commit()


def generate_id(title, link):
    return hashlib.md5((title + link).encode()).hexdigest()


def is_sent(post_id):
    cursor.execute("SELECT 1 FROM posts WHERE id=?", (post_id,))
    return cursor.fetchone()


def save(post_id):
    try:
        cursor.execute("INSERT INTO posts VALUES (?)", (post_id,))
        conn.commit()
    except:
        pass