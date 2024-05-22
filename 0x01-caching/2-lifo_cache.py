#!/usr/bin/python3
"""A class LIFOCache that inherits from BaseCaching"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Create a class LIFOCache"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            if key in self.cache_data:
                # Remove the existing key from stack to update its position
                self.stack.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Evict the last item added to the cache (LIFO)
                last_key = self.stack.pop()
                del self.cache_data[last_key]
                print(f"DISCARD: {last_key}")

            self.cache_data[key] = item
            self.stack.append(key)

    def get(self, key):
        """Get an item by key"""
        return self.cache_data.get(key, None)
