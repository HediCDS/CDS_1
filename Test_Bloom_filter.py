from Testing import BloomFilter
from random import shuffle
import random
import string
from typing import List

exp_count = 1000
fp_rate = 0.05

def get_words(ln: int) -> str:
    charachters = string.ascii_lowercase
    rndom = [random.choice(charachters) for _ in range(ln)]
    return "".join(rndom)

def list_words(exp_count: int, words: List, min=3, max=12) -> List[str]:
    list = set()
    for i in range(exp_count):
        string = get_words(random.randint(min, max))
        if string not in words:
            list.add(string)
    return list(list)

def test_bf():
    words_to_insert = list_words(exp_count)
    bf = BloomFilter(exp_count, fp_rate)
    for word in words_to_insert:
        bf.insert(word)
    shuffle(words_to_insert)
    for word in words_to_insert:
        if not bf.search(word):
            print('Error, cannot have false negatives.')
            return
    print("No false negatives")
    
    not_added = list_words(exp_count, words_to_insert)
    for word in words_to_insert:
        if bf.search(word):
            if word in not_added:
                print(f'{word} is a false positive')
            else:
                print(f'{word} is probably present')
        else:
            print(f'{word} is not present')
