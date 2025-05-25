import argparse
import os
import sys
from scraper.crawler import Crawler
from scraper.downloader import Downloader
from scraper.utils.colors import Colors
from scraper.url_support import UrlSupport

# ðŸ§¼ Fallbacks fÃ¼r Farben (wenn die Source sie nicht definiert)
setattr(Colors, 'FAIL', getattr(Colors, 'RED', ''))
setattr(Colors, 'WARNING', getattr(Colors, 'YELLOW', ''))

# ðŸŽ¯ Einzelne URL verarbeiten
def process_single_url(url, output):
    urlType = UrlSupport.getType(url)
    Colors.print(f"ðŸ”Ž URL-Typ erkannt: {urlType}", Colors.CYAN)

    if urlType not in ['season', 'movie', 'episode']:
        Colors.print(f"âš ï¸ Nicht unterstÃ¼tzter URL-Typ oder ungÃ¼ltige URL: {url}", Colors.FAIL)
        return

    crawler = Crawler()
    links = crawler.crawl(url)

    if not links:
        Colors.print("ðŸš« Keine Links zum Download gefunden.", Colors.FAIL)
        return

    downloader = Downloader()
    for item in links:
        folder_name = item.get('subfolder', 'default')
        path = os.path.join(output, folder_name)
        Colors.print(f"â¬‡ï¸ Download startet: {folder_name}", Colors.YELLOW)
        downloader.downloadUrls(path, item['links'])

# ðŸ“¦ Mehrere URLs aus Datei verarbeiten (batch)
def process_batch(file_path, forced_type, output):
    crawler = Crawler()
    downloader = Downloader()

    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    Colors.print(f"ðŸ“¦ Batch-Verarbeitung gestartet: {len(urls)} URLs", Colors.CYAN)

    for idx, url in enumerate(urls, start=1):
        url_type = forced_type or UrlSupport().getType(url)

        if url_type not in ['season', 'movie', 'episode']:
            Colors.print(f"âš ï¸ [{idx}] UngÃ¼ltiger oder unbekannter URL-Typ: {url}", Colors.FAIL)
            continue

        emoji = {
            'season': 'ðŸ“º',
            'movie': 'ðŸŽ¥',
            'episode': 'ðŸ“„'
        }.get(url_type, 'ðŸ“¦')

        Colors.print(f"{emoji} [{idx}/{len(urls)}] Verarbeite ({url_type}): {url}", Colors.BLUE)

        links = crawler.crawl(url)

        if not links:
            Colors.print("âš ï¸ Keine Links gefunden. Ãœberspringe.", Colors.WARNING)
            continue

        for item in links:
            folder_name = item.get('subfolder', f"{url_type}_{idx}")
            path = os.path.join(output, folder_name)
            Colors.print(f"â¬‡ï¸ Download startet: {folder_name}", Colors.YELLOW)
            downloader.downloadUrls(path, item['links'])

    Colors.print("âœ… Batch abgeschlossen.", Colors.GREEN)

# ðŸ§  Verbesserter Parser mit Farbe bei Fehlern
class CustomHelpParser(argparse.ArgumentParser):
    def error(self, message):
        Colors.print(f"âŒ Fehler: {message}", Colors.FAIL)
        self.print_help()
        sys.exit(2)

# ðŸ§­ Argumente
parser = CustomHelpParser(
    description="ðŸŽ¬ Fancaps Downloader CLI â€“ powered by deiner groÃŸen Schwester ðŸ˜Ž",
    usage="python fancaps-downloader.py [URL] [--output DIR] [--batch-type {season,movie}] [--batch-file FILE]"
)

parser.add_argument('url', nargs='?', help='Einzelne URL zum Download (season/movie/episode)')
parser.add_argument('--output', type=str, default="Downloads", help='Zielordner fÃ¼r Downloads')
parser.add_argument('--batch-type', type=str, choices=['season', 'movie'], help='Typ der Inhalte im Batch-Modus (optional)')
parser.add_argument('--batch-file', type=str, help='Pfad zur Textdatei mit URLs')
parser.add_argument('-?', action='help', help='Zeigt diese Hilfe an')

args = parser.parse_args()

# ðŸš€ Main-Logik
if __name__ == "__main__":
    if args.batch_file:
        process_batch(args.batch_file, args.batch_type, args.output)
    elif args.url:
        process_single_url(args.url, args.output)
    else:
        Colors.print("âŒ Keine URL oder Batch-Parameter angegeben.", Colors.FAIL)
        parser.print_help()
