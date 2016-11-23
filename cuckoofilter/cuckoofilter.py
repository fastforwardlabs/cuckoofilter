import mmh3  # murmur hashing
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

        # initialize the entire table.
        for i in range(self.filter_capacity):
            self.table.append(cuckootable.CuckooTable(size=self.bucket_size))

    # fingerprint of an item is a reduced bit string of
    # of an input string.
    def obtain_fingerprint(self, string_item):
        hash_value = mmh3.hash_bytes(string_item)
        fingerprint = hash_value[:self.item_fingerprint_size]
        return fingerprint

    def obtain_index_from_hash(self, string_item):

        hash_value = mmh3.hash_bytes(string_item)

        # this is new for python 3, i.e. how you go from
        # bytes/bits to int/index values
        index = int.from_bytes(hash_value, byteorder="big")

        # modulo the obtained index by the filter capacity
        # this helps to restrict indices to 0 - filter_capacity
        index = index % self.filter_capacity

        return index

    def obtain_indices_from_item(self, string_item):

        # obtain the first index
        index_1 = self.obtain_index_from_hash(string_item)

        # obtain finger print of item
        fingerprint = self.obtain_fingerprint(string_item)

        # derive the index from the fingerprint
        # second index -> first_index xor index
        # derived from hash(fingerprint)
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

        # obtain the two possible indices where this item
        # can be inserted.
        index_1, index_2 = self.obtain_indices_from_item(item_to_insert)
        item_fingerprint = self.obtain_fingerprint(item_to_insert)

        # default is to insert into the first index.
        if self.table[index_1].insert(item_fingerprint):
            self.cuckoo_size += 1
            return index_1

        # if the first location is occupied, then insert
        # in the second location.
        if self.table[index_2].insert(item_fingerprint):
            self.cuckoo_size += 1
            return index_2

        # if both indices are full, now we need to swap all current entries.
        # first randomly pick btw index 1 and 2
        # then swap one item in that bucket for its
        # alternative location.
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

        # Notifies that the table is now full.
        raise Exception("CuckooFilter has filled up!")

    def remove(self, item_to_remove):
        # first hash the item and obtain its possible indices
        item_fingerprint = self.obtain_fingerprint(item_to_remove)
        index_1, index_2 = self.obtain_indices_from_item(item_to_remove)

        # check the first index to see if item's fingerprint
        # is in that bucket.
        if self.table[index_1].remove(item_fingerprint):
            self.cuckoo_size = self.cuckoo_size - 1
            return True

        # item not in first index, so now check the second index
        if self.table[index_2].remove(item_fingerprint):
            self.cuckoo_size = self.cuckoo_size - 1
            return True

        # since item not in both indices, it is not in the
        # cuckoo table. return false.
        return False

    def __contains__(self, item_to_test):
        item_fingerprint = self.obtain_fingerprint(item_to_test)

        index_1, index_2 = self.obtain_indices_from_item(item_to_test)

        bool_contains = (item_fingerprint in self.table[index_1]) or (
            item_fingerprint in self.table[index_2])

        return bool_contains

    """

    The methods below are getters for various properties of the 
    CuckooFilter. 
    - load factor 
    - size
    - capacity 

    """

    def get_load_factor(self):
        load_factor = self.cuckoo_size / \
            (self.filter_capacity * self.bucket_size)
        return load_factor

    def get_size(self):
        return self.cuckoo_size

    def get_capacity(self):
        return self.filter_capacity
