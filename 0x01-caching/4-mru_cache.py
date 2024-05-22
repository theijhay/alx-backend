#!/usr/bin/python3
"""A class MRUCache that inherits from BaseCaching"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Create a class MRUCache that inherits from BaseCaching"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """Add an item in the cache"""
        if key is not None and item is not None:
            if key in self.cache_data:
                # Remove the existing key from order to update its position
                self.order.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Evict the most recently used item (MRU)
                mru_key = self.order.pop()
                del self.cache_data[mru_key]
                print(f"DISCARD: {mru_key}")

            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """Get an item by key"""
        if key in self.cache_data:
            # Move the accessed key to the end to mark it as recently used
            self.order.remove(key)
            self.order.append(key)
            return self.cache_data[key]
        return None
