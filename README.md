# Cuckoo Filter

The Fast Forward Labs team explored probabilistic data structures
in our "Probabilistic Methods for Real-time Streams" report and 
prototype (contact us if you're interested in this topic). We 
provided an update to that report [here](http://blog.fastforwardlabs.com/post/153566952648/cuckoo-filter), exploring
Cuckoo filters, a [new](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf) probabilistic data structure that improves upon the standard Bloom filter. The Cuckoo filter provides a few 
advantages: 
1) it enables dynamic deletion and addition of items 
2) it can be easily implemented compared to Bloom filter variants with similar capabilities, and 
3) for similar space constraints, the Cuckoo filter provides lower false positives, particularly at lower capacities. We provide a python implementation of the  Cuckoo filter here, and compare it to a counting Bloom filter (a Bloom filter variant).

This repository contains a python implementation of the Cuckoo
filter, as well as a copy-paste of a counting Bloom filter from 
the [fuggedaboutit](https://github.com/mynameisfiber/fuggetaboutit/) repository for benchmarking. 

Please see our [post](http://blog.fastforwardlabs.com/post/153566952648/cuckoo-filter) for more details on the
Cuckoo filter. 


# Demo

Below we show how to go about using this package. 

```python
>>> from cuckoofilter import CuckooFilter
>>> c_filter = CuckooFilter(10000, 2)

>>> c_filter.insert('James')
>>> print("James in c_filter == {}".format("James" in c_filter))
James in c_filter == True

>>> c_filter.remove('James')
>>> print("James in c_filter == {}".format("James" in c_filter))
James in c_filter == False
```

Similarly, the counting Bloom filter can be used as well.

```python
>>> from cuckoofilter import CountingBloomFilter
>>> b_filter = CountingBloomFilter(10000)

>>> b_filter.add('James')
>>> print("James in c_filter == {}".format("James" in c_filter))
James in b_filter == True

>>> b_filter.remove('James')
>>> print("James in c_filter == {}".format("James" in c_filter))
James in b_filter == False
``` 

## References
Below we link to a few references that contributed to the work 
shown here: 

- Fan et. al. [Cuckoo Filter: Practically Better Than Bloom](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf)

- CS 166 Stanford lecture [Cuckoo Hashing](http://web.stanford.edu/class/cs166/lectures/13/Small13.pdf)

- Charles Ren, Course Notes. [An Overview of Cuckoo Hashing](http://cs.stanford.edu/~rishig/courses/ref/l13a.pdf)




