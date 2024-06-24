#import necessary packages
import math
import mmh3
from bitarray import bitarray
import typing

class BloomFilter:
    #BloomFilter class using mmh3 hash functions
    def __init__(self, exp_count: int, fp_rate: float):
        """exp_count: expected number of words to be inserted in the bloom filter.
           fp_rate: probability of false positives"""
        #Fpositive probability 
        self.fp_rate = fp_rate
        
        #size of the array that will be used
        self.size = self.compute_size(exp_count, self.fp_rate)

        #number of hash functions that will be used
        self.hfunctions = self.compute_hash_count(self.size, exp_count)

        #set number of inserted words to 0
        self.strings_count = 0

        #create the array and fill it with zeros
        self.array = bitarray(self.size)
        self.array.setall(0)


    def insert(self, string: str) -> None:
        """insert string to the bloom filter"""
        
        for i in range(self.hfunctions):
            #use hash functions to generate corresponding positions in the array
            set = mmh3.hash(string, i) % self.size
            #fill the positions with 1
            self.array[set] = 1
        #increment the counter of inserted words
        self.strings_count += 1

    def search(self, string: str)-> bool:
        """search for a string in the bloom using hash functions"""
        for i in range(self.hfunctions):
            set = mmh3.hash(string, i) % self.size
            #if any of the corresponding positions in the array = 0, 100% the string is not there.
            if not self.array[set]:
                return False
        #if all positions of this string are 1, it is probably in the bloom
        return True
    
    def count_strings(self) -> int:
        """Keep track of the inserted strings"""
        return self.strings_count

    def compute_size(self, count, prob) -> int:
        """count: expected number of strings to be inserted
           prob: prob of false positives"""
        #use the count and the prob to calculate the size of array
        size = - (count * math.log(prob)) / (math.log(2) ** 2)
        return int(size)

    def compute_hash_count(self, arraysize: int, exp_words: int) -> int:
        """arraysize: the computed size of the array
           exp_words: expected number of strings to be inserted"""
        
        #use the array size and the expected count of strings to calculate number of hash functions
        hash_count = (arraysize / exp_words) * math.log(2)
        return int(hash_count)
    
