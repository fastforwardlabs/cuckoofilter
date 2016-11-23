"""
We represent the buckets as lists. A numpy array with
pre-specified length might be better, but the 
python list is quite flexible. 
"""

import random


class CuckooTable:

    def __init__(self, size=4):
        self.size = size
        self.bucket = []

    def insert(self, item_fingerprint):
        # to insert a fingerprint, check to make sure the
        # current bucket is not full.
        if len(self.bucket) < self.size:
            self.bucket.append(item_fingerprint)
            return True

        # bucket is full, so return false. cuckoo filter class
        # handles the logic with a failed insert.
        return False

    def remove(self, item_fingerprint):
        # first check if the fingerprint is in this bucket.
        # if yes, then return true, else return false.
        try:
            index = self.bucket.index(item_fingerprint)
            del self.bucket[index]
            return True
        except ValueError:
            return False

    # We implement swapping as a method of the bucket class
    # to make it easier when performing swaps.

    def swap_fingerprints(self, item_fingerprint):
        # we need to select the index of the fingerprint to swap.
        index_to_select = random.randrange(0, len(self.bucket))
        selected_fingerprint = self.bucket[index_to_select]

        # now swap
        item_fingerprint, self.bucket[
            index_to_select] = selected_fingerprint, item_fingerprint

        return item_fingerprint

    # check if an item is in a bucket, i.e, list.
    def __contains__(self, item_fingerprint):
        if item_fingerprint in self.bucket:
            return True
        return False
