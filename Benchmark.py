from Bloom_filter import BloomFilter
import random
import time
import string
import matplotlib.pyplot as plt

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

def benchmark(nlist, p):
  time_insert = []
  time_search = []
  prob_fpos = []
  for n in nlist:
    bf = BloomFilter(n, p)
    strings_inserted = list_words(n, set())

    begin_time = time.time()
    for string in strings_inserted:
      bf.insert(string)
    time_ins = time.time() - begin_time
    time_insert.append(time_ins)

