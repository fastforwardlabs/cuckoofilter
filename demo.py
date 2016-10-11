from cuckoofilter import CuckooFilter

if __name__ == "__main__":

    max_items = 100000
    c_filter = CuckooFilter(max_items, 2)

    num_inserted = 0

    for i in range(max_items):
        try:
            c_filter.insert(str(i))
            num_inserted = num_inserted + 1
        except:
            print("number of items inserted -->> " + str(num_inserted))
            break

    print("number of items inserted -->> " + str(num_inserted))

    for i in range(num_inserted):
        assert str(i) in c_filter

    total_queries = 0
    false_queries = 0

    for i in range(max_items, 10*max_items):
        if str(i) in c_filter:
            false_queries = false_queries + 1

        total_queries = total_queries + 1

    print('False positive rate is {:%}'.format(false_queries / total_queries))
