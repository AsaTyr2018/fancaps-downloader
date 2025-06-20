from importlib import import_module

# Re-export core modules
Crawler = import_module('scraper.crawler').Crawler
AltCrawler = import_module('scraper.alt_crawler').AltCrawler
Downloader = import_module('scraper.downloader').Downloader
UrlSupport = import_module('scraper.url_support').UrlSupport
Colors = import_module('scraper.utils.colors').Colors

__all__ = ['Crawler', 'AltCrawler', 'Downloader', 'UrlSupport', 'Colors']
