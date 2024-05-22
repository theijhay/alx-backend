#!/usr/bin/env python3
"""A class FIFOCache that inherits from BaseCachin"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """Create a class FIFOCache"""

    def __init__(self):
        """Initialize"""
        super().__init__()
        self.key_indexes = []

    def put(self, key, item):
        """Assign the item value for the key in the cache"""
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                return key

            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                item_discarded = self.key_indexes.pop(0)
                del self.cache_data[item_discarded]
                print("DISCARD:", item_discarded)

            self.cache_data[key] = item
            self.key_indexes.append(key)

    def get(self, key):
        """Return the value linked to the key in the cache"""
        if key in self.cache_data:
            return self.cache_data[key]
        return None
