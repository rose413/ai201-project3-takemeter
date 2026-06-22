import requests
import pandas as pd
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

# ==============================
# CONFIG
# ==============================
session = requests.Session()
BASE_URL = "https://old.reddit.com/r/truezelda/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
TARGET_PER_CLASS = 100
MAX_SUBREDDIT_PAGES = 15
REQUEST_DELAY = 1.0

# ==============================
# LABELING
# ==============================

ARGUMENT_PATTERNS = [
    r"\bbecause\b", r"\bsince\b", r"\btherefore\b",
    r"\bthus\b", r"\bevidence\b", r"\bsuggests\b",
    r"\bimplies\b", r"\bfor example\b", r"\bthis shows\b",
    r"\bas a result\b", r"\btherefore\b"
]

OPINION_PATTERNS = [
    r"\bi think\b", r"\bi feel\b", r"\bi believe\b",
    r"\bmy favorite\b", r"\bpersonally\b", r"\bi like\b",
    r"\bi love\b", r"\bi hate\b", r"\bbest\b",
    r"\bworst\b", r"\benjoy\b"
]

def classify(text):
    t = text.lower()

    has_arg = any(re.search(p, t) for p in ARGUMENT_PATTERNS)
    has_op = any(re.search(p, t) for p in OPINION_PATTERNS)

    if has_arg:
        return "argument", "contains reasoning"
    if has_op:
        return "opinion", ""

    if len(t.split()) < 6:
        return "opinion", "very short"

    return "opinion", "default"

# ==============================
# STORAGE
# ==============================

arguments = []
opinions = []
seen = set()

# ==============================
# HELPERS
# ==============================

def clean(text):
    return re.sub(r"\s+", " ", text).strip()

def add(text):
    global arguments, opinions, seen

    text = clean(text)

    if not text or text in seen:
        return

    seen.add(text)

    label, notes = classify(text)

    row = {
        "text": text,
        "label": label,
        "notes": notes
    }

    if label == "argument" and len(arguments) < TARGET_PER_CLASS:
        arguments.append(row)

    elif label == "opinion" and len(opinions) < TARGET_PER_CLASS:
        opinions.append(row)

# ==============================
# COMMENT SCRAPER (RECURSIVE)
# ==============================

def scrape_comments(comment_url):
    try:
        r = requests.get(comment_url, headers=HEADERS)
        soup = BeautifulSoup(r.text, "html.parser")

        # comment bodies
        for md in soup.find_all("div", class_="md"):
            text = md.get_text(strip=True)
            add(text)

        # follow "more comments" links if present
        more_links = soup.find_all("a", string=re.compile("more comments", re.I))

        for link in more_links:
            href = urljoin(comment_url, link["href"])
            scrape_comments(href)

    except Exception:
        return

# ==============================
# POST SCRAPER
# ==============================

def scrape_subreddit_page(url):
    res = requests.get(url, headers=HEADERS)  
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    posts = soup.find_all("div", attrs={"data-fullname": True})

    next_button = soup.find("span", class_="next-button")
    next_url = next_button.a["href"] if next_button else None

    for post in posts:

        if len(arguments) >= TARGET_PER_CLASS and len(opinions) >= TARGET_PER_CLASS:
            break

        try:
            title = post.find("a", class_="title")
            if title:
                add(title.text)

            comments_link = post.find("a", string=re.compile("comment", re.I))
            if comments_link:
                scrape_comments(comments_link["href"])

        except Exception:
            continue
    print(res.status_code)
    print(res.text[:1000])
    return next_url

# ==============================
# MAIN LOOP
# ==============================

print("Starting scrape of r/truezelda...")

url = BASE_URL
page = 0

while url and page < MAX_SUBREDDIT_PAGES:

    if len(arguments) >= TARGET_PER_CLASS and len(opinions) >= TARGET_PER_CLASS:
        break

    print(f"Scraping page {page + 1}")

    url = scrape_subreddit_page(url)

    page += 1
    time.sleep(REQUEST_DELAY)

# ==============================
# FINAL DATASET
# ==============================

dataset = arguments[:TARGET_PER_CLASS] + opinions[:TARGET_PER_CLASS]

df = pd.DataFrame(dataset)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("truezelda_argument_opinion_dataset.csv", index=False)

# ==============================
# SUMMARY
# ==============================

print("\nDONE")
print(f"Arguments: {len(arguments)}")
print(f"Opinions: {len(opinions)}")
print("Saved: truezelda_argument_opinion_dataset.csv")