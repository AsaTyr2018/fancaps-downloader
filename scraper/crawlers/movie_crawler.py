"""Crawler for movie screenshots."""

import re
from bs4 import BeautifulSoup
import cloudscraper
from scraper.utils.url_utils import thumb_to_cdn

class MovieCrawler:
    def crawl(self, url):
        picLinks = []
        currentUrl = url
        pageNumber = 1
        alt = None

        try:
            # Extract subfolder name from URL
            match = re.search(r"https://fancaps.net\/.*\?name=(.*)&", url)
            if match:
                subfolder = match.group(1)
            else:
                raise ValueError("URL does not contain a valid subfolder name.")
        except ValueError as e:
            print(f"Error extracting subfolder: {e}")
            return

        thumb_pattern = re.compile(r"^https://moviethumbs.*?fancaps\.net/")

        scraper = cloudscraper.create_scraper()

        while currentUrl:
            try:
                response = scraper.get(currentUrl, timeout=10)
                if 'cf-browser-verification' in response.text:
                    print('Cloudflare challenge detected. Aborting.')
                    break
                beautifulSoup = BeautifulSoup(response.text, "html.parser")
            except Exception as e:
                print(f"Error fetching page: {e}")
                break

            for img in beautifulSoup.find_all("img", src=thumb_pattern):
                imgSrc = img.get("src")
                imgAlt = img.get("alt")
                if not alt:
                    alt = imgAlt
                if alt == imgAlt:
                    picLinks.append(thumb_to_cdn(imgSrc))

            try:
                # Generate and verify the existence of the next page URL
                next = url.replace(f'https://fancaps.net/movies/','') +f"&page={pageNumber + 1}"
                nextPage = beautifulSoup.find("a", href=next)
                if nextPage:
                    pageNumber += 1
                    currentUrl = url + f"&page={pageNumber}"
                else:
                    currentUrl = None
            except Exception as e:
                print(f"Error processing next page: {e}")
                break

        return {
            'subfolder': subfolder,
            'links': picLinks
        }
