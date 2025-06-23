"""Primary crawler for Fancaps URLs."""

from scraper.url_support import UrlSupport
from scraper.crawlers import episode_crawler, season_crawler, movie_crawler
from scraper.utils.colors import Colors
from bs4 import BeautifulSoup
import cloudscraper
from urllib.parse import urljoin

class Crawler:
    def crawl(self, url, visited=None):
        """Crawl a fancaps URL or generic page for image links."""
        if visited is None:
            visited = set()
        if url in visited:
            return []
        visited.add(url)

        Colors.print(f"{url} crawling started:", Colors.YELLOW)

        url_support = UrlSupport()
        url_type = url_support.getType(url)

        if url_type == 'season':
            print(f"\t\"{url_type}\" url detected")
            crawler = season_crawler.SeasonCrawler()
            output = crawler.crawl(url)
        elif url_type == 'episode':
            print(f"\t\"{url_type}\" url detected")
            crawler = episode_crawler.EpisodeCrawler()
            output = [crawler.crawl(url)]
        elif url_type == 'movie':
            print(f"\t\"{url_type}\" url detected")
            crawler = movie_crawler.MovieCrawler()
            output = [crawler.crawl(url)]
        else:
            # Generic page handling: find supported links and crawl them
            Colors.print("\tGeneric page detected. Searching for links...", Colors.BLUE)
            output = []
            scraper = cloudscraper.create_scraper()
            try:
                response = scraper.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                Colors.print(f"Error opening {url}: {e}", Colors.RED)
                return []

            for anchor in soup.find_all('a', href=True):
                link = urljoin(url, anchor['href'])
                if url_support.getType(link):
                    output.extend(self.crawl(link, visited))

        Colors.print(f"{url} crawling finished.", Colors.YELLOW)

        empty = True
        for item in output:
            if item.get('links'):
                empty = False
            else:
                Colors.print("No images found for this entry. The page may be blocked or invalid.", Colors.WARNING)
        if empty:
            Colors.print("No image links parsed from URL. Possible blocking or invalid URL.", Colors.WARNING)
        return output
