import argparse
import os
import sys
from scraper.crawler import Crawler
from scraper.downloader import Downloader
from scraper.utils.colors import Colors
from scraper.url_support import UrlSupport

setattr(Colors, 'FAIL', getattr(Colors, 'RED', ''))
setattr(Colors, 'WARNING', getattr(Colors, 'YELLOW', ''))

def process_single_url(url, output):
    urlType = UrlSupport.getType(url)
    Colors.print(f"ðŸ”Ž URL-Typ: {urlType}", Colors.CYAN)

    if urlType not in ['season', 'movie', 'episode']:
        Colors.print(f"âš ï¸ Not supported Typ or Invalide URL: {url}", Colors.FAIL)
        return

    crawler = Crawler()
    links = crawler.crawl(url)

    if not links:
        Colors.print("ðŸš« No Links found.", Colors.FAIL)
        return

    downloader = Downloader()
    for item in links:
        folder_name = item.get('subfolder', 'default')
        path = os.path.join(output, folder_name)
        Colors.print(f"â¬‡ï¸ Download startet: {folder_name}", Colors.YELLOW)
        downloader.downloadUrls(path, item['links'])

def process_batch(file_path, forced_type, output):
    crawler = Crawler()
    downloader = Downloader()

    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    Colors.print(f"ðŸ“¦ Batch started: {len(urls)} URLs", Colors.CYAN)

    for idx, url in enumerate(urls, start=1):
        url_type = forced_type or UrlSupport().getType(url)

        if url_type not in ['season', 'movie', 'episode']:
            Colors.print(f"âš ï¸ [{idx}] Not supported Typ or Invalide URL: {url}", Colors.FAIL)
            continue

        emoji = {
            'season': 'ðŸ“º',
            'movie': 'ðŸŽ¥',
            'episode': 'ðŸ“„'
        }.get(url_type, 'ðŸ“¦')

        Colors.print(f"{emoji} [{idx}/{len(urls)}] Proccessing ({url_type}): {url}", Colors.BLUE)

        links = crawler.crawl(url)

        if not links:
            Colors.print("âš ï¸ No Links found.", Colors.WARNING)
            continue

        for item in links:
            folder_name = item.get('subfolder', f"{url_type}_{idx}")
            path = os.path.join(output, folder_name)
            Colors.print(f"â¬‡ï¸ Download startet: {folder_name}", Colors.YELLOW)
            downloader.downloadUrls(path, item['links'])

    Colors.print("âœ… Batch Done.", Colors.GREEN)

class CustomHelpParser(argparse.ArgumentParser):
    def error(self, message):
        Colors.print(f"âŒ Fehler: {message}", Colors.FAIL)
        self.print_help()
        sys.exit(2)

parser = CustomHelpParser(
    description="ðŸŽ¬ Fancaps Downloader CLI â€“ powered by Asatyr ðŸ˜Ž",
    usage="python fancaps-downloader.py [URL] [--output DIR] [--batch-type {season,movie}] [--batch-file FILE]"
)

parser.add_argument('url', nargs='?', help='Single URL Mode (season/movie/episode)')
parser.add_argument('--output', type=str, default="Downloads", help='Target folder for Downloads')
parser.add_argument('--batch-type', type=str, choices=['season', 'movie'], help='Typ of downloads (optional)')
parser.add_argument('--batch-file', type=str, help='Path to txt file of URLs')
parser.add_argument('-?', action='help', help='Show help')

args = parser.parse_args()

if __name__ == "__main__":
    if args.batch_file:
        process_batch(args.batch_file, args.batch_type, args.output)
    elif args.url:
        process_single_url(args.url, args.output)
    else:
        Colors.print("âŒ Missing parameter.", Colors.FAIL)
        parser.print_help()
