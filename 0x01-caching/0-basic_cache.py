#!/usr/bin/python3
"""A class BasicCache that inherits from BaseCaching and is a caching system"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    def put(self, key, item):
        """Assign the item value for the key in the cache"""
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """Return the value linked to the key in the cache"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
