import time
import re
import threading
from flask import Flask

from config import WEBSITES
from scraper import scrape
from database import generate_id, is_sent, save
from sender import send
from utils import detect_category, get_image

# 🌐 Dummy server (Render ke liye)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# 🔥 KEYWORDS FILTER
KEYWORDS = ["vacancy", "result", "admit", "apply", "exam", "notification"]

def is_important(title):
    if not title:
        return False
    return any(word in title.lower() for word in KEYWORDS)

def clean_title(title):
    if not title:
        return ""
    title = title.lower()
    title = re.sub(r'[^a-z0-9 ]', '', title)
    return title.strip()

def make_summary(title):
    if not title:
        return ""
    return " ".join(title.split()[:10]) + "..."

def format_msg(title, link, category):
    summary = make_summary(title)

    return f"""
🔥 <b>GenZ CyberHub</b>

📰 <b>{title}</b>

📌 {summary}

📂 Category: <b>{category}</b>
🔗 <a href="{link}">Read Full Update</a>

━━━━━━━━━━━━━━━
🚀 Join: @GenZcyberhub
"""

def run():
    print("Checking...")

    for site in WEBSITES:
        data = scrape(site["url"])
        print(f"{site['name']} → {len(data)} items")

        for title, link in data[:20]:

            if not title or not link:
                continue

            
            post_id = generate_id(link)

            

            category = detect_category(title)
            msg = format_msg(title, link, category)

            image = get_image(link)

            try:
                send(msg, image)
                save(post_id)
                print("✅ Sent:", title[:50])

            except Exception as e:
                print("❌ Error:", e)

    print("Done\n")


# 🔁 BOT LOOP (thread me chalega)
def start_bot():
    while True:
        try:
            run()
            time.sleep(300)

        except Exception as e:
            print("Crash prevented:", e)
            time.sleep(60)


if __name__ == "__main__":
    # ✅ bot ko background me chalao
    threading.Thread(target=start_bot).start()

    # ✅ Render ko satisfy karo (PORT IMPORTANT)
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)