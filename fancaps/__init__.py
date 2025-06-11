from importlib import import_module

# Re-export core modules
Crawler = import_module('scraper.crawler').Crawler
Downloader = import_module('scraper.downloader').Downloader
UrlSupport = import_module('scraper.url_support').UrlSupport
Colors = import_module('scraper.utils.colors').Colors

__all__ = ['Crawler', 'Downloader', 'UrlSupport', 'Colors']
