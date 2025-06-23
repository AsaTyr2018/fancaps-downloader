"""Crawler for TV and anime seasons."""

from bs4 import BeautifulSoup
from scraper.crawlers import episode_crawler
import re
import cloudscraper
from scraper.utils.colors import Colors

class SeasonCrawler:
    url = None
    name = None

    def crawl(self, url):
        epLinks = []
        picLinks = []
        self.url = url
        currentUrl = self.url
        page = 1

        scraper = cloudscraper.create_scraper()

        while currentUrl:
            try:
                response = scraper.get(currentUrl, timeout=10)
                if 'cf-browser-verification' in response.text:
                    Colors.print('Cloudflare challenge detected. Aborting.', Colors.RED)
                    break
                beautifulSoup = BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                Colors.print(f"Error occurred while fetching the page: {e}", Colors.RED)
                break

            for DOMLink in beautifulSoup.find_all('a', class_='btn', href=re.compile(r"^.*?/episodeimages.php\?")):
                href = DOMLink.get('href')
                if href:
                    if not re.match(r"^https://.*?/episodeimages.php\?", href):
                        href = 'https://fancaps.net' + DOMLink.get('href')

                    match = re.search(r"https://fancaps.net/.*?/episodeimages.php\?\d+-(.*?)/", href)
                    if match:
                        if not self.name:
                            self.name = match.group(1)
                        if self.name == match.group(1):
                            epLinks.append(href)
            if beautifulSoup.find("a", text=re.compile(r'Next', re.IGNORECASE), href=lambda href: href and href != "#"):
                page += 1
                currentUrl = url + f"&page={page}"
            else:
                currentUrl = None

        crawler = episode_crawler.EpisodeCrawler()
        for epLink in epLinks:
            try:
                episodeResult = crawler.crawl(epLink)
                picLinks.append(episodeResult)
                Colors.print(f"\t{epLink} crawled", Colors.GREEN)
            except Exception as e:
                Colors.print(f"Failed to crawl {epLink}: {e}", Colors.RED)

        return picLinks
