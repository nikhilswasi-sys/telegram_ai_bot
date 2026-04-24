import time
import re
from config import WEBSITES
from scraper import scrape
from database import generate_id, is_sent, save
from sender import send
from utils import detect_category, get_image

# 🔥 KEYWORDS FILTER (simple & effective)
KEYWORDS = ["vacancy", "result", "admit", "apply", "exam", "notification"]

def is_important(title):
    if not title:
        return False
    return any(word in title.lower() for word in KEYWORDS)

# 🔥 CLEAN TITLE (optional - ab use nahi ho raha id me)
def clean_title(title):
    if not title:
        return ""
    title = title.lower()
    title = re.sub(r'[^a-z0-9 ]', '', title)
    return title.strip()

# 🔥 SIMPLE SUMMARY
def make_summary(title):
    if not title:
        return ""
    return " ".join(title.split()[:10]) + "..."

# 🔥 FINAL MESSAGE FORMAT (channel branding)
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

            # ✅ Safety check
            if not title or not link:
                continue

            # ✅ important filter
            if not is_important(title):
                continue

            # ✅ FIXED (IMPORTANT 🔥)
            post_id = generate_id(link)

            if is_sent(post_id):
                continue

            category = detect_category(title)
            msg = format_msg(title, link, category)

            # 🔥 AUTO THUMBNAIL
            image = get_image(link)

            try:
                send(msg, image)
                save(post_id)
                print("✅ Sent:", title[:50])

            except Exception as e:
                print("❌ Error:", e)

    print("Done\n")


# 🔁 LOOP (auto run every 5 min)
while True:
    try:
        run()
        time.sleep(300)

    except Exception as e:
        print("Crash prevented:", e)
        time.sleep(60)