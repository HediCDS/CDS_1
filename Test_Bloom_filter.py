from Bloom_filter import BloomFilter
from random import shuffle
import random
import string
import mmh3
from typing import List
import numpy as np

exp_count = 1000
exp_fp_rate = 0.05

def get_words(ln: int) -> str:
    charachters = string.ascii_lowercase
    rndom = [random.choice(charachters) for _ in range(ln)]
    return "".join(rndom)

def get_DNA(ln: int):
    letters = 'ATCG'
    return "".join(random.choice(letters) for _ in range(ln))

def list_words(exp_count: int, words, min=3, max=12) -> List[str]:
    wlist = set()
    for i in range(exp_count):
        string = get_words(random.randint(min, max))
        if string not in words:
            wlist.add(string)
    return list(wlist)

def dna_generator(n, min=10, max=100):
    return [get_DNA(random.randint(min, max)) for _ in range(n)]

def words_generator(n, min=3, max=12):
    return [get_words(random.randint(min, max)) for _ in range(n)]


def test_hashF():
    b = BloomFilter(exp_count, exp_fp_rate)
    strings = words_generator(exp_count)
    print("Hash functions test: natural language")
    for i in range(b.hfunctions):
        hashes = [mmh3.hash(string, i) % b.size for string in strings]
        print(f'Function {i+1}: Minimum length = {min(hashes)}, Maximum length = {max(hashes)}, Mean={sum(hashes)/len(hashes)}, Standard deviation={np.std(hashes):.2f}')

    print("Hash functions test: DNA sequences")
    dna_seq = dna_generator(exp_count)
    for i in range(b.hfunctions):
        hashes = [mmh3.hash(dna, i) % b.size for dna in dna_seq]
        print(f'Function {i+1}: Minimum length = {min(hashes)}, Maximum length = {max(hashes)}, Mean={sum(hashes)/len(hashes)}, Standard deviation={np.std(hashes):.2f}')

def test_bf():
    words_to_insert = list_words(exp_count, set())
    bf = BloomFilter(exp_count, exp_fp_rate)
    for word in words_to_insert:
        bf.insert(word)
    shuffle(words_to_insert)
    for word in words_to_insert:
        if not bf.search(word):
            print('Error, cannot have false negatives.')
            return
    print("No false negatives")
    
    not_added = list_words(exp_count, words_to_insert)
    f_pos = 0
    for word in not_added:
        if bf.search(word):
            f_pos += 1
    fp_prob = f_pos / len(not_added)
    print(f'Actual false positive rate = {fp_prob:.2f}')
    if fp_prob > bf.fp_rate:
        print('Caution, the actual false positive rate exceeded the expected')
