from Bloom_filter import BloomFilter
from random import shuffle
import random
import string
from typing import List

exp_count = 1000
exp_fp_rate = 0.05

def get_words(ln: int) -> str:
    charachters = string.ascii_lowercase
    rndom = [random.choice(charachters) for _ in range(ln)]
    return "".join(rndom)

def list_words(exp_count: int, words, min=3, max=12) -> List[str]:
    wlist = set()
    for i in range(exp_count):
        string = get_words(random.randint(min, max))
        if string not in words:
            wlist.add(string)
    return list(wlist)

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
    
