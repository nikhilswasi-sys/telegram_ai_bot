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


# ✅ FIXED: only link needed
def generate_id(link):
    if not link:
        return None
    return hashlib.md5(link.encode()).hexdigest()


def is_sent(post_id):
    if not post_id:
        return False

    cursor.execute("SELECT 1 FROM posts WHERE id=?", (post_id,))
    return cursor.fetchone() is not None


def save(post_id):
    if not post_id:
        return

    try:
        cursor.execute("INSERT INTO posts VALUES (?)", (post_id,))
        conn.commit()
    except:
        pass