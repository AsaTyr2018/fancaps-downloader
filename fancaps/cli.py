"""Command line interface for the Fancaps framework."""
import argparse
import os
from . import Crawler, AltCrawler, Downloader, Colors, UrlSupport


def process_single_url(url: str, output: str, alt: bool = False) -> None:
    url_type = UrlSupport().getType(url)
    Colors.print(f"URL-Typ: {url_type}", Colors.CYAN)

    if url_type not in {"season", "movie", "episode"}:
        Colors.print(f"Unsupported or invalid URL: {url}", Colors.FAIL)
        return

    crawler = AltCrawler() if alt else Crawler()
    links = crawler.crawl(url)
    if not links:
        Colors.print("No links found.", Colors.FAIL)
        return

    downloader = Downloader()
    for item in links:
        folder_name = item.get("subfolder", "default")
        path = os.path.join(output, folder_name)
        Colors.print(f"Download startet: {folder_name}", Colors.YELLOW)
        downloader.downloadUrls(path, item["links"])


def process_batch(file_path: str, forced_type: str, output: str, alt: bool = False) -> None:
    crawler = AltCrawler() if alt else Crawler()
    downloader = Downloader()

    with open(file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    Colors.print(f"Batch started: {len(urls)} URLs", Colors.CYAN)

    for idx, url in enumerate(urls, start=1):
        url_type = forced_type or UrlSupport().getType(url)
        if url_type not in {"season", "movie", "episode"}:
            Colors.print(f"[{idx}] Unsupported or invalid URL: {url}", Colors.FAIL)
            continue

        links = crawler.crawl(url)
        if not links:
            Colors.print("No links found.", Colors.WARNING)
            continue

        for item in links:
            folder_name = item.get("subfolder", f"{url_type}_{idx}")
            path = os.path.join(output, folder_name)
            Colors.print(f"Download startet: {folder_name}", Colors.YELLOW)
            downloader.downloadUrls(path, item["links"])

    Colors.print("Batch Done.", Colors.GREEN)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Fancaps Downloader CLI",
        usage="python -m fancaps.cli [URL] [--output DIR] [--batch-type {season,movie}] [--batch-file FILE] [--alt]",
    )
    parser.add_argument("url", nargs="?", help="Single URL Mode (season/movie/episode)")
    parser.add_argument("--output", type=str, default="Downloads", help="Target folder for downloads")
    parser.add_argument("--batch-type", type=str, choices=["season", "movie"], help="Type of downloads (optional)")
    parser.add_argument("--batch-file", type=str, help="Path to txt file of URLs")
    parser.add_argument("--alt", action="store_true", help="Use alternative crawler")

    args = parser.parse_args(argv)

    if args.batch_file:
        process_batch(args.batch_file, args.batch_type, args.output, args.alt)
    elif args.url:
        process_single_url(args.url, args.output, args.alt)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
