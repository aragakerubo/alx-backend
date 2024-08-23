#!usr/bin/env python3
"""this module contains the implementation of
a fifo cache"""
BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """class inherits from basecaching and implements the fifo type
    of cache"""

    def __init__(self):
        """the init method that initialises the created object"""
        super().__init__()
        self.__cache_list = []

    def put(self, key, item):
        """the method adds an element to the cache and
        replaces one based on which one came in first"""
        if key is None or item is None:
            return
        if key not in self.__cache_list:
            self.__cache_list.insert(0, key)
        else:
            key_index = self.__cache_list.index(key)
            del self.__cache_list[key_index]
            self.__cache_list.insert(0, key)
        if len(self.__cache_list) > self.MAX_ITEMS:
            replace = self.__cache_list.pop()
            del self.cache_data[replace]
            print("DISCARD: {}".format(replace))
        self.cache_data[key] = item

    def get(self, key):
        """method retunrd the item related to the key
        passed as an argument"""
        if key is None:
            return None
        item = self.cache_data.get(key)
        if item is None:
            return None
        return item
