import re
from bs4 import BeautifulSoup
import cloudscraper
import os
from scraper.utils.url_utils import thumb_to_cdn

class EpisodeCrawler:
    def crawl(self, url):
        picLinks = []  # List to store the picture links
        currentUrl = url  # Current URL to crawl
        pageNumber = 1  # Initialize page number
        alt = None  # Initialize alt attribute value for images

        # Extract episode type, subfolder information from URL
        match = re.search(r"https://fancaps.net\/([a-zA-Z]+)\/.*\?\d+-(.*?)/(.*)", url)
        if not match:
            print("Invalid URL format.")
            return {"subfolder": "", "links": []}

        epType = match.group(1)  # Episode type (tv or anime)
        subfolder = os.path.join(match.group(2), match.group(3))  # Construct subfolder path

        # Build dynamic regex for thumbnail host
        thumb_pattern = re.compile(rf"^https://{epType}thumbs.*?fancaps\.net/")

        scraper = cloudscraper.create_scraper()

        while currentUrl:
            try:
                response = scraper.get(currentUrl, timeout=10)
                if 'cf-browser-verification' in response.text:
                    print('Cloudflare challenge detected. Aborting.')
                    break
            except Exception as e:
                print(f"Error opening URL: {e}")
                break

            try:
                beautifulSoup = BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                print(f"Error parsing page: {e}")
                break

            # Find all image tags with a specific source pattern
            for img in beautifulSoup.find_all("img", src=thumb_pattern):
                imgSrc = img.get("src")
                imgAlt = img.get("alt")
                if not alt:
                    alt = imgAlt  # Set alt if not already set
                if alt == imgAlt:
                    picLinks.append(thumb_to_cdn(imgSrc))

            # Check for a next page link
            nextPage = beautifulSoup.find("a", href=lambda href: href and f"&page={pageNumber + 1}" in href)
            if nextPage:
                pageNumber += 1  # Increment page number
                currentUrl = f"{url}&page={pageNumber}"  # Update current URL
            else:
                currentUrl = None  # No more pages, stop crawling

        return {
            'subfolder': subfolder,  # Return subfolder path
            'links': picLinks  # Return list of picture links
        }

