#!/usr/bin/env python3

import requests
import time
import redis

class WebCache:
    def __init__(self, host='localhost', port=6379):
        self._redis = redis.Redis(host=host, port=port, decode_responses=True)
    
    def get_page(self, url: str) -> str:
        # Check if the URL is already cached
        cached_content = self._redis.get(url)
        if cached_content:
            print(f"Cache hit for URL: {url}")
            return cached_content
        
        # Fetch the page content
        response = requests.get(url)
        page_content = response.text
        
        # Cache the content with a 10-second expiration
        self._redis.setex(url, 10, page_content)
        
        # Track URL access count
        self._redis.incr(f"count:{url}")
        
        return page_content

    def get_access_count(self, url: str) -> int:
        # Get the access count for the URL
        count = self._redis.get(f"count:{url}")
        return int(count) if count else 0

# Usage example
web_cache = WebCache()

# Access a slow URL
url = "http://slowwly.robertomurray.co.uk/delay/10000/url/https://www.example.com"
content = web_cache.get_page(url)
print(content)

# Access the same URL again (should be cached)
content = web_cache.get_page(url)
print(content)

# Access count for the URL
access_count = web_cache.get_access_count(url)
print(f"Access count for {url}: {access_count}")
