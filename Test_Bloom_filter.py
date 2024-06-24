#import necessary packages
from Bloom_filter import BloomFilter
from random import shuffle
import random
import string
import mmh3
from typing import List
import numpy as np

#specify expected number of strings to be inserted and the expected false positive rate.
exp_count = 1000
exp_fp_rate = 0.05

#Function to provide lowercase strings of given length
def get_words(ln: int) -> str:
    charachters = string.ascii_lowercase
    rndom = [random.choice(charachters) for _ in range(ln)]
    return "".join(rndom)
    
#Function to generate DNA sequences
def get_DNA(ln: int):
    letters = 'ATCG'
    return "".join(random.choice(letters) for _ in range(ln))

#Function to provide strings that are unique from the inserted ones, this to test false positives
def list_words(exp_count: int, words, min=3, max=12) -> List[str]:
    wlist = set()
    for i in range(exp_count):
        string = get_words(random.randint(min, max))
        if string not in words:
            wlist.add(string)
    return list(wlist)

#Function to list the generated DNA sequences
def dna_generator(n, min=10, max=100):
    return [get_DNA(random.randint(min, max)) for _ in range(n)]

#Function to list the generated words
def words_generator(n, min=3, max=12):
    return [get_words(random.randint(min, max)) for _ in range(n)]

#Function to test the hash functions
def test_hashF():
    #create a bloom filter with the expected count and fp probability
    b = BloomFilter(exp_count, exp_fp_rate)
    #Domain1: generate natural language words
    strings = words_generator(exp_count)
    print("Hash functions test: natural language")
    for i in range(b.hfunctions):
        hashes = [mmh3.hash(string, i) % b.size for string in strings]
        #The dist of each hash function for natural language
        print(f'Function {i+1}: Minimum length = {min(hashes)}, Maximum length = {max(hashes)}, Mean={sum(hashes)/len(hashes)}, Standard deviation={np.std(hashes):.2f}')

    #Domain2: DNA sequences
    print("Hash functions test: DNA sequences")
    dna_seq = dna_generator(exp_count)
    for i in range(b.hfunctions):
        hashes = [mmh3.hash(dna, i) % b.size for dna in dna_seq]
        #The dist of hash functions for DNA sequences
        print(f'Function {i+1}: Minimum length = {min(hashes)}, Maximum length = {max(hashes)}, Mean={sum(hashes)/len(hashes)}, Standard deviation={np.std(hashes):.2f}')

#Function to test false positives and false negatives
def test_bf():
    #get a list of strings to be inserted
    words_to_insert = list_words(exp_count, set())

    #create an object of the bloom filter
    bf = BloomFilter(exp_count, exp_fp_rate)

    #insert the generated words in the bloom
    for word in words_to_insert:
        bf.insert(word)

    #shuffle the strings
    shuffle(words_to_insert)

    #If all inserted words are in the bloom, no problem. Otherwise, print an Error msg, cannot have false negatives
    for word in words_to_insert:
        if not bf.search(word):
            print('Error, cannot have false negatives.')
            return
    print("No false negatives")

    #get another list of words and make sure that they have not been inserted
    not_added = list_words(exp_count, set(words_to_insert))
    
    #set the counter of false positives to 0
    f_pos = 0
    #increment the false positives counter whenever you face a false positve
    for word in not_added:
        if bf.search(word):
            f_pos += 1

    #calculate and print the actual false positive rate
    fp_prob = f_pos / len(not_added)
    print(f'Actual false positive rate = {fp_prob:.2f}')

    #print a warning msg if the actual false positive prob exceed the expected
    if fp_prob > bf.fp_rate:
        print('Caution, the actual false positive rate exceeded the expected')
