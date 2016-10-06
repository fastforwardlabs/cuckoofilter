"""
In this script, we test different methods of generating 
the fingerprint for a particular item. 

In get_indices_from_string, we mod the hash value of the
with the fingerprint value that we want. 

In original_get_indices_from_string, we chop off part of the
byte representation of the hash to the original size that we 
want. 

"""

import mmh3
import random
import numpy as np

_finger_print_size = 2
_filter_capacity = 10000


def get_indices_from_string(item):
    hash_value = mmh3.hash_bytes(str(item))
    first_index = int.from_bytes(hash_value, byteorder="big")

    fingerprint = first_index % (2**_finger_print_size)
    first_index = first_index % _filter_capacity

    hash_value_finger_print = mmh3.hash_bytes(str(fingerprint))
    index_fingerprint = int.from_bytes(
        hash_value_finger_print, byteorder="big")

    index_fingerprint = index_fingerprint % _filter_capacity

    second_index = index_fingerprint ^ first_index
    second_index = second_index % _filter_capacity

    return first_index, second_index


def original_get_indices_from_string(item):
    hash_value = mmh3.hash_bytes(str(item))

    fingerprint = hash_value[:_finger_print_size]  # the key change

    first_index = int.from_bytes(hash_value, byteorder="big")
    first_index = first_index % _filter_capacity

    hash_value_finger_print = mmh3.hash_bytes(fingerprint)
    index_fingerprint = int.from_bytes(
        hash_value_finger_print, byteorder="big")

    index_fingerprint = index_fingerprint % _filter_capacity

    second_index = index_fingerprint ^ first_index
    second_index = second_index % _filter_capacity

    return first_index, second_index


def main():

    test_strings = ["james", "micha", "mike", "grant", "nick",
                    "kathryn", "hilary", "frederiche",
                    "aditya", "julius", "danielle"]

    for val in test_strings:
        print(get_indices_from_string(val))
        print(original_get_indices_from_string(val))

    print()
    print()

    integers = np.random.random_integers(0, 100, 10)

    for val in integers:
        print(get_indices_from_string(str(val)))
        print(original_get_indices_from_string(str(val)))

if __name__ == "__main__":
    main()
