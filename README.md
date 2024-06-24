# CDS_1
Bloom Filter is a space-efficient-probabilistic data structure. It is used to test whether an element is a member of 
a set or not. It makes use of bit arrays and hash functions for insertion and search of elements. Bloom Filter usually comes with a trade-off between efficiency and accuracy. This means that there is a probability of false positives. For example, if the Bloof Filter says that it has inserted a given string, this means that it might or might not br inserted. However, there is no place for false negatives in a bloom filter. So, if the bloom says that a given element does not exist, we are 100% sure it doesn't exist. The lower the false positive rate a user tolerates, the larger the array used for insertion, hence more storage needed, and more hash functions also. Inserting 10,000 word requires larger array than inserting 500 words, so the aim is to find the balance between efficiency and accuracy.

This repository includes:
1- Bloom_filter.py: A module that contains the BloomFilter class with insert, search and count strings methods.
This file is the file which contains the implementation of the bloom filter algorithm.

2- test_Bloom_filter.py: A test file to test the distribution of the hash functions, whether the algorithm is accurate about the false negatives, and whether the actual false positive rate exceeds what is expected or not.

3- benchmark.py: A performance test for the bloom filter methods with large sample sizes. Using visualization, we assess the insertion and search times as a function of increasing words counts, as well as assesing changes in the compression rate nad false positive rates as a function of increasing words counts. This script is furhter used in the HPC infrastructure to test and do experiments.


Conclusions:
- On average, as the number of inserted words increases, the time needed for insertion increases.
- On average, as the number of inserted words increases, the time needed for searching increases.
- There are some unstable changes in the false positive rate as a function of increasing words counts, we can see that it decreases drastically between 20,000 to 50,000 words, followed by dramatic increase as word counts increase.
- The compression rate decreases with increasing word counts untill a certain count (about 50,000 word) which it remains stable after.
