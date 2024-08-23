#!/usr/bin/env python3
"""this module contains class BasicClass that inherits
from BaseCaching"""
BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """BasicCaching inherits from BaseCaching and implements the two
    unimplemented methods put and get in BaseCaching"""

    def __init__(self):
        """the init method that initialises the created object"""
        super().__init__()

    def put(self, key, item):
        """this method assigns to the dictionary in the
        super class BaseCaching called cache_data

        Args:
                key (str): the key for the data that will be put in the cache
                item (string): the item associated with the key
        """
        if (key and item) is not None:
            self.cache_data[key] = item

    def get(self, key):
        """this method returns a given entry in the dictionary for a key"""
        if key is None:
            return None
        item = self.cache_data.get(key)
        if item is None:
            return None
        return item
