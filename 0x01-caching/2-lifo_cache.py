#!usr/bin/env python3
"""this module contains a class that implements the lifo
type of cache system"""
BaseCaching = __import__("base_caching").BaseCaching


class LIFOCache(BaseCaching):
    """this class implements the lifo type of cashe
    and inherits from basecaching"""

    def __init__(self):
        """the method that initialises an object made from this class"""
        super().__init__()
        self.__cache_list = []

    def put(self, key, item):
        """function that adds an element to the cache_data in
        the super class"""
        if key is None or item is None:
            return
        if key not in self.__cache_list:
            self.__cache_list.append(key)
        else:
            key_index = self.__cache_list.index(key)
            del self.__cache_list[key_index]
            self.__cache_list.append(key)
        if len(self.__cache_list) > self.MAX_ITEMS:
            replacement = self.__cache_list.pop(-2)
            del self.cache_data[replacement]
            print("DISCARD: {}".format(replacement))
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
