import mmh3  # used for hashing items
import random

from . import cuckootable


class CuckooFilter:

    def __init__(self, filter_capacity,
                 item_fingerprint_size, num_swaps=500, bucket_size=4):

        self.filter_capacity = filter_capacity
        self.item_fingerprint_size = item_fingerprint_size
        self.num_swaps = num_swaps
        self.bucket_size = bucket_size
        self.cuckoo_size = 0
        self.table = []

        # load factor
        # initialize the entire table.
        for i in range(self.filter_capacity):
            self.table.append(cuckootable.CuckooTable(size=self.bucket_size))

    def obtain_fingerprint(self, string_item):
        hash_value = mmh3.hash_bytes(string_item)
        fingerprint = hash_value[:self.item_fingerprint_size]
        return fingerprint

    def obtain_index_from_hash(self, string_item):
        hash_value = mmh3.hash_bytes(string_item)
        index = int.from_bytes(hash_value, byteorder="big")
        index = index % self.filter_capacity
        return index

    def obtain_indices_from_item(self, string_item):
        # insert into the cuckoo table
        index_1 = self.obtain_index_from_hash(string_item)

        fingerprint = self.obtain_fingerprint(string_item)

        index_2 = index_1 ^ self.obtain_index_from_hash(fingerprint)
        index_2 = index_2 % self.filter_capacity

        return index_1, index_2

    def insert(self, item):
        """Here for legacy reasons... use .add"""
        return self.add(item)

    def add(self, item_to_insert):
        # check that item_to_insert is a string.
        if not isinstance(item_to_insert, str):
            raise ValueError("Item being inserted not of type string")

        index_1, index_2 = self.obtain_indices_from_item(item_to_insert)
        item_fingerprint = self.obtain_fingerprint(item_to_insert)

        if self.table[index_1].insert(item_fingerprint):
            self.cuckoo_size += 1
            return index_1

        if self.table[index_2].insert(item_fingerprint):
            self.cuckoo_size += 1
            return index_2

        # if both indices are full, now we need to swap all current entries.
        # first randomly pick btw index 1 and 2
        random_index = random.choice((index_1, index_2))

        for swap in range(self.num_swaps):
            item_fingerprint = self.table[
                random_index].swap_fingerprints(item_fingerprint)

            random_index = random_index ^ self.obtain_index_from_hash(
                item_fingerprint)
            random_index = random_index % self.filter_capacity

            if self.table[random_index].insert(item_fingerprint):
                self.cuckoo_size += 1
                return random_index

        # this might not be necessary since the table is now full anyway
        raise Exception("CuckooFilter has filled up!")

    def remove(self, item_to_remove):
        item_fingerprint = self.obtain_fingerprint(item_to_remove)
        index_1, index_2 = self.obtain_indices_from_item(item_to_remove)

        if self.table[index_1].remove(item_fingerprint):
            self.cuckoo_size = self.cuckoo_size - 1
            return True

        if self.table[index_2].remove(item_fingerprint):
            self.cuckoo_size = self.cuckoo_size - 1
            return True

        return False

    def __contains__(self, item_to_test):
        item_fingerprint = self.obtain_fingerprint(item_to_test)

        index_1, index_2 = self.obtain_indices_from_item(item_to_test)

        bool_contains = (item_fingerprint in self.table[index_1]) or (
            item_fingerprint in self.table[index_2])

        return bool_contains

    def get_load_factor(self):
        load_factor = self.size / (self.filter_capacity * self.bucket_size)
        return load_factor

    def get_size(self):
        return self.cuckoo_size

    def get_capacity(self):
        return self.filter_capacity
