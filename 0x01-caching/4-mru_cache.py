#!usr/bin/env python3
"""this module contains a clas that implements the mru type
of caching system"""
BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """this class inherits from base caching and implements the
    mru type of caching system"""

    def __init__(self):
        """the init method which initialises an object"""
        super().__init__()
        self.__cache_list = []

    def put(self, key, item):
        """implements the mru typ of caching when the list is greater
        than the max size"""
        if key is None or item is None:
            return
        if key not in self.__cache_list:
            self.__cache_list.append(key)
        else:
            key_index = self.__cache_list.index(key)
            del self.__cache_list[key_index]
            self.__cache_list.append(key)
        if len(self.__cache_list) > self.MAX_ITEMS:
            print("DISCARD: {}".format(self.__cache_list[-2]))
            del self.cache_data[self.__cache_list[-2]]
            del self.__cache_list[-2]
        self.cache_data[key] = item

    def get(self, key):
        """method retunrd the item related to the key
        passed as an argument"""
        if key is None:
            return None
        item = self.cache_data.get(key)
        if item is None:
            return None
        key_index = self.__cache_list.index(key)
        del self.__cache_list[key_index]
        self.__cache_list.append(key)
        return item
