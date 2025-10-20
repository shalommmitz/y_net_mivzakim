import feedparser
import hashlib
import os
import time
import datetime
import shutil

# RSS feed for "starship" on Google News
RSS_FEED_URL = "https://news.google.com/rss/search?q=starship"

# File to store seen article hashes
SEEN_FILE = "seen_articles.txt"

# Load seen articles from file
def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(line.strip() for line in f)

# Save seen articles to file
def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        for article_hash in seen:
            f.write(f"{article_hash}\n")

# Generate a hash for an article (based on title and link)
def article_hash(entry):
    key = f"{entry.title}{entry.link}"
    return hashlib.sha256(key.encode()).hexdigest()

# Fetch articles
def fetch_google_items():
    feed = feedparser.parse(RSS_FEED_URL)

    time_stamps = []
    headers = []
    links = []

    for entry in feed.entries:
        dt = time.mktime(entry.published_parsed)
        dt = datetime.datetime.fromtimestamp(dt)
        time_stamps.append(dt)
        headers.append(entry.title)
        links.append(entry.link)

    return time_stamps, headers, links
    
if __name__ == "__main__":
    term_width = shutil.get_terminal_size((80, 20)).columns
    print("📰 New 'Starship' Headlines:\n")
    time_stamps, headers, links = fetch_google_items()
    for idx in range(len(headers)):
        ts = time_stamps[idx].strftime("%H:%M")
        print(f"{ts} {headers[idx][:term_width]}\n")
    if len(headers)==0:
        print("No new headlines since last check.")

