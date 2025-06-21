import re
import os
import concurrent.futures

# Limit for concurrent workers used by the alternative crawler.  A lower default
# prevents hitting the "Too many open files" error when nested thread pools are
# created.
DEFAULT_MAX_WORKERS = 10
from bs4 import BeautifulSoup
import cloudscraper
from urllib.parse import urljoin
from scraper.utils.colors import Colors
from scraper.url_support import UrlSupport


class AltEpisodeCrawler:
    def crawl(self, url, max_workers=DEFAULT_MAX_WORKERS):
        pic_links = []
        picture_pages = []
        page_number = 1
        current_url = url

        match = re.search(r"https://fancaps.net/([a-zA-Z]+)/episodeimages.php\?\d+-(.*?)/(.*)", url)
        subfolder = ""
        if match:
            subfolder = os.path.join(match.group(2), match.group(3))

        scraper = cloudscraper.create_scraper()

        while current_url:
            try:
                response = scraper.get(current_url, timeout=10)
                if "cf-browser-verification" in response.text:
                    Colors.print("Cloudflare challenge detected. Aborting.", Colors.RED)
                    break
                soup = BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                Colors.print(f"Error opening {current_url}: {e}", Colors.RED)
                break

            anchors = soup.find_all("a", href=lambda href: href and "picture.php" in href)
            for a in anchors:
                link = a.get("href")
                if not link.startswith("http"):
                    link = urljoin("https://fancaps.net", link)
                picture_pages.append(link)

            next_page = soup.find(
                "a",
                href=lambda href: href
                and f"&page={page_number + 1}" in href
                and href != "#",
            )
            if next_page:
                page_number += 1
                current_url = f"{url}&page={page_number}"
            else:
                current_url = None

        def fetch_image(link):
            # Create a new scraper per image and close it after use to avoid
            # leaving open file descriptors.
            with cloudscraper.create_scraper() as local_scraper:
                try:
                    r = local_scraper.get(link, timeout=10)
                    img_soup = BeautifulSoup(r.text, "html.parser")
                    img = img_soup.find("img", id="imageTag")
                    if img:
                        return img.get("src")
                except Exception as e:
                    Colors.print(f"Failed to fetch image {link}: {e}", Colors.RED)
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(fetch_image, p) for p in picture_pages]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    pic_links.append(result)

        return {
            "subfolder": subfolder,
            "links": pic_links,
        }


class AltSeasonCrawler:
    def crawl(self, url, max_workers=DEFAULT_MAX_WORKERS):
        ep_links = []
        pic_links = []
        page = 1
        current_url = url
        scraper = cloudscraper.create_scraper()
        name = None

        while current_url:
            try:
                response = scraper.get(current_url, timeout=10)
                if "cf-browser-verification" in response.text:
                    Colors.print("Cloudflare challenge detected. Aborting.", Colors.RED)
                    break
                soup = BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                Colors.print(f"Error occurred while fetching the page: {e}", Colors.RED)
                break

            for DOMLink in soup.find_all("a", class_="btn", href=re.compile(r"^.*?/episodeimages.php\?")):
                href = DOMLink.get("href")
                if href and not href.startswith("http"):
                    href = "https://fancaps.net" + href
                match = re.search(r"https://fancaps.net/.*/episodeimages.php\?\d+-(.*?)/", href or "")
                if match:
                    if not name:
                        name = match.group(1)
                    if name == match.group(1):
                        ep_links.append(href)

            next_button = soup.find(
                "a",
                text=re.compile(r"Next", re.IGNORECASE),
                href=lambda href: href and href != "#",
            )
            if next_button:
                page += 1
                current_url = url + f"&page={page}"
            else:
                current_url = None

        def crawl_episode(link):
            crawler = AltEpisodeCrawler()
            return crawler.crawl(link, max_workers=max_workers)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(crawl_episode, l): l for l in ep_links}
            for future in concurrent.futures.as_completed(futures):
                link = futures[future]
                try:
                    episode_result = future.result()
                    pic_links.append(episode_result)
                    Colors.print(f"\t{link} crawled", Colors.GREEN)
                except Exception as e:
                    Colors.print(f"Failed to crawl {link}: {e}", Colors.RED)

        return pic_links


class AltCrawler:
    def crawl(self, url, visited=None, max_workers=DEFAULT_MAX_WORKERS):
        if visited is None:
            visited = set()
        if url in visited:
            return []
        visited.add(url)

        Colors.print(f"{url} crawling started (alt):", Colors.YELLOW)

        url_support = UrlSupport()
        url_type = url_support.getType(url)

        if url_type == "season":
            crawler = AltSeasonCrawler()
            output = crawler.crawl(url, max_workers=max_workers)
        elif url_type == "episode":
            crawler = AltEpisodeCrawler()
            output = [crawler.crawl(url, max_workers=max_workers)]
        else:
            Colors.print("Alternative crawler only supports season or episode URLs.", Colors.RED)
            output = []

        Colors.print(f"{url} crawling finished.", Colors.YELLOW)

        empty = True
        for item in output:
            if item.get("links"):
                empty = False
            else:
                Colors.print("No images found for this entry. The page may be blocked or invalid.", Colors.WARNING)
        if empty:
            Colors.print("No image links parsed from URL. Possible blocking or invalid URL.", Colors.WARNING)
        return output

