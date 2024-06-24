import math
import mmh3
from bitarray import bitarray
import typing

class BloomFilter:
    def __init__(self, exp_count, fp_rate):
        self.fp_rate = fp_rate
        self.size = self.compute_size(exp_count, self.fp_rate)
        self.hfunctions = self.compute_hash_count(self.size, exp_count)
        self.strings_count = 0
        self.array = bitarray(self.size)
        self.array.setall(0)

    def insert(self, string: str) -> None:
        for i in range(self.hfunctions):
            set = mmh3.hash(string, i) % self.size
            self.array[set] = 1
        self.strings_count += 1

    def search(self, string: str)-> bool:
        for i in range(self.hfunctions):
            set = mmh3.hash(string, i) % self.size
            if not self.array[set]:
                return False
        return True
    
    def count_strings(self) -> int:
        return self.strings_count
    
    def compute_size(self, count, prob) -> int:
        size = - (count * math.log(prob)) / (math.log(2) ** 2)
        return int(size)
    
    def compute_hash_count(self, arraysize: int, exp_words: int) -> int:
        hash_count = (arraysize / exp_words) * math.log(2)
        return int(hash_count)
    
