import re
from urllib.parse import urlparse, urlunparse


def thumb_to_cdn(url: str) -> str:
    """Convert a thumbnail URL to its CDN counterpart.

    This replaces the "thumbs" subdomain segment with "cdn" while preserving
    any additional subdomain parts (e.g. tvthumbs1 -> tvcdn1).
    """
    parsed = urlparse(url)
    cdn_host = re.sub(r"thumbs", "cdn", parsed.netloc, count=1)
    return urlunparse(parsed._replace(netloc=cdn_host))
