from urllib.parse import urlparse, urlunparse


def thumb_to_cdn(url: str) -> str:
    """Convert a thumbnail URL to the current CDN host.

    The provider previously served images from per-category hosts like
    ``animecdn`` or ``tvcdn``. These domains are no longer reachable and all
    images are now served from ``cdni.fancaps.net``.  Only the hostname
    changes, the path remains untouched.
    """

    parsed = urlparse(url)
    # Replace any old thumbnail or CDN host with the new generic one
    return urlunparse(parsed._replace(netloc="cdni.fancaps.net"))
