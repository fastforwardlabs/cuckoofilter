import unittest
from cuckoofilter import CuckooFilter


class CuckooFilterTest(unittest.TestCase):

    def setUp(self):
        self.capacity = 1000
        self.fingerprint_size = 2
        self.cuckoofilter = CuckooFilter(self.capacity, self.fingerprint_size)

    def test_cuckoo_filter_creation(self):

        # test to cuckoo filter creation
        self.assertIsNotNone(self.cuckoofilter)

        # check that it uses the input arguments.
        self.assertEqual(self.capacity, self.cuckoofilter.get_capacity())

    def test_insertions(self):
        # insert a string into the cuckoo filter
        initial_size = self.cuckoofilter.get_size()

        self.cuckoofilter.insert("James")

        self.assertEqual(initial_size + 1, self.cuckoofilter.get_size())

    def test_deletions(self):
        self.cuckoofilter.insert("New")

        self.assertTrue(self.cuckoofilter.remove("New"))

        self.assertFalse("New" in self.cuckoofilter)

        # test deleting an element that was not inserted
        self.assertFalse(self.cuckoofilter.remove("Not inserted"))

    def test_containing(self):

        self.cuckoofilter.insert("finally")

        self.assertTrue("finally" in self.cuckoofilter)

    def test_that_cuckoo_filter_fills_up(self):

        with self.assertRaises(Exception) as context:
            for i in range(10*self.capacity):
                self.cuckoofilter.insert(str(i))

        self.assertTrue(
            "CuckooFilter has filled up!" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
