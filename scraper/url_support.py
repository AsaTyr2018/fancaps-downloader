import re

class UrlSupport:
    reSupportedUrls = {
        'season': r"https://fancaps.net/(.*?)/showimages.php.*?", 
        'episode': r"https://fancaps.net/(.*?)/episodeimages.php.*?", 
        'movie': r"https://fancaps.net/movies/MovieImages.php.*?" 
    }


    def getType(self, url):
        for url_type, pattern in self.reSupportedUrls.items():
            if re.search(pattern, url):
                return url_type
        return None
