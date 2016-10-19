from cuckoofilter import CuckooFilter
from cuckoofilter import CountingBloomFilter

if __name__ == "__main__":

    max_items = 10000
    c_filter = CuckooFilter(2*max_items, 2)
    b_filter = CountingBloomFilter(2*max_items)

    num_inserted = 0
    for i in range(max_items):
        try:
            c_filter.insert(str(i))
            b_filter.add(str(i))
            num_inserted = num_inserted + 1
        except: #the exception here is for the cuckoo filter. 
            print("number of items inserted -->> " + str(num_inserted))
            break


    print("number of items inserted -->> " + str(num_inserted))
    print("size of the bloom filter is  -->> " + str(int(b_filter.get_size())))
    print("size of the cuckoo filter is  -->> " + str(int(c_filter.get_size())))

    print()

    for i in range(num_inserted):
        assert str(i) in c_filter
        assert str(i) in b_filter

    print("done asserting that inserted values are indeed in the filters")

    total_queries = 0
    false_queries_cuckoo = 0
    false_queries_bloom = 0 

    for i in range(max_items, 10*max_items):
        if str(i) in c_filter:
            false_queries_cuckoo += 1

        if str(i) in b_filter:
            false_queries_bloom += 1

        total_queries = total_queries + 1

    print('Cuckoo filter false positive rate is {:%}'.format(false_queries_cuckoo / total_queries))
    print('Counting bloom filter false positive rate is {:%}'.format(false_queries_bloom / total_queries))

