from config import KEYWORDS
import requests
from bs4 import BeautifulSoup

def detect_category(title):
    title = title.lower()

    for category, words in KEYWORDS.items():
        if any(w in title for w in words):
            return category

    return "UPDATE"


# 🔥 AUTO THUMBNAIL FUNCTION
def get_image(link):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(link, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ Try og:image (best case)
        img = soup.find("meta", property="og:image")
        if img and img.get("content"):
            return img.get("content")

        # ⚠️ fallback: first image on page
        img_tag = soup.find("img")
        if img_tag and img_tag.get("src"):
            return img_tag.get("src")

    except Exception as e:
        print("Image fetch error:", e)

    return None