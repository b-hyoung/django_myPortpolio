from email.utils import parsedate_to_datetime
from html import unescape
import re
import urllib.request
import xml.etree.ElementTree as ET

from django.core.cache import cache


TISTORY_RSS_URL = "https://kimbob-world.tistory.com/rss"


def _strip_html(text):
    if not text:
        return ""
    no_tags = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", unescape(no_tags)).strip()


def fetch_tistory_posts(limit=5, cache_seconds=600):
    cache_key = f"tistory_posts_{limit}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        req = urllib.request.Request(TISTORY_RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            xml_data = resp.read()

        root = ET.fromstring(xml_data)
        channel = root.find("channel")
        if channel is None:
            cache.set(cache_key, [], cache_seconds)
            return []

        posts = []
        for item in channel.findall("item")[:limit]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            description = _strip_html(item.findtext("description") or "")
            pub_date_raw = (item.findtext("pubDate") or "").strip()

            published = ""
            if pub_date_raw:
                try:
                    dt = parsedate_to_datetime(pub_date_raw)
                    published = dt.strftime("%Y-%m-%d")
                except Exception:
                    published = pub_date_raw

            posts.append(
                {
                    "title": title,
                    "url": link,
                    "summary": description,
                    "published": published,
                    "source": "tistory",
                }
            )

        cache.set(cache_key, posts, cache_seconds)
        return posts
    except Exception:
        cache.set(cache_key, [], cache_seconds)
        return []
