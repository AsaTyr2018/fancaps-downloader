import time
import os
import logging
from scraper.crawler import Crawler
from scraper.downloader import Downloader
from scraper.utils.colors import Colors
from scraper.url_support import UrlSupport

QUEUE_FILE = "/opt/fancaps/queue.txt"
ARCHIVE_FILE = "/opt/fancaps/archive.txt"
LOG_FILE = "/var/log/fancaps-daemon.log"
OUTPUT_DIR = "/opt/fancaps/downloads"
INTERVAL_SECONDS = 300  # 5 Minuten


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


setattr(Colors, 'print', lambda msg, *_: logging.info(msg))

def read_first_url():
    if not os.path.exists(QUEUE_FILE):
        return None
    with open(QUEUE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0] if lines else None

def remove_url_from_queue(url):
    with open(QUEUE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    lines = [line for line in lines if line != url]
    with open(QUEUE_FILE, "w") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))

def append_to_archive(url):
    with open(ARCHIVE_FILE, "a") as f:
        f.write(url + "\n")

def process_single_url(url):
    url_type = UrlSupport().getType(url)
    Colors.print(f"🔎 URL-Typ: {url_type}")

    if url_type not in ['season', 'movie', 'episode']:
        Colors.print(f"⚠️ Not supported URL-Typ or invalid URL: {url}")
        return False

    crawler = Crawler()
    links = crawler.crawl(url)

    if not links:
        Colors.print("🚫 No links to download found.")
        return False

    downloader = Downloader()
    for item in links:
        folder_name = item.get('subfolder', 'default')
        path = os.path.join(OUTPUT_DIR, folder_name)
        Colors.print(f"⬇️ Download startet: {folder_name}")
        downloader.downloadUrls(path, item['links'])

    Colors.print(f"✅ Batch done for: {url}")
    return True

def daemon_loop():
    Colors.print("🌀 Fancaps Daemon Started")
    while True:
        url = read_first_url()
        if url:
            Colors.print(f"📥 New URL found: {url}")
            success = process_single_url(url)
            if success:
                remove_url_from_queue(url)
                append_to_archive(url)
        else:
            Colors.print("📭 No new URLs. Starting Loop...")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        daemon_loop()
    except KeyboardInterrupt:
        Colors.print("👋 Daemon wurde manuell beendet.")
