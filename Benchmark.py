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
        strings_check_list = strings_inserted[:n // 2] + list_words(n // 2, set(strings_inserted)) 
        begin_search_time = time.time()
        fp = 0
        for s in strings_check_list:
            if bf.search(s) and s not in strings_inserted:
                fp += 1
        check_time = time.time() - begin_search_time
        time_search.append(check_time)  
        fprate = fp / (n // 2)
        prob_fpos.append(fprate)
    return time_insert, time_search, prob_fpos


nlist = [1000, 5000, 10000, 50000, 100000]
fprate = 0.05

time_insert, time_search, prob_fp = benchmark(nlist, fprate)

plt.figure(figsize=(14, 8))

plt.subplot(1, 3, 1)
plt.plot(nlist, time_insert, label = "Insertion Time")
plt.xlabel('Words Counts')
plt.ylabel('Time in seconds')
plt.legend()


plt.subplot(1, 3, 1)
plt.plot(nlist, time_insert, label = "Insertion Time")
plt.title('Insert Time')
plt.xlabel('Words Counts')
plt.ylabel('Time in seconds')
plt.legend()


plt.subplot(1, 3, 1)
plt.plot(nlist, time_search, label = "Search Time")
plt.title('Search Time')
plt.xlabel('Words Counts')
plt.ylabel('Time in seconds')
plt.legend()

plt.subplot(1, 3, 1)
plt.plot(nlist, prob_fp, label = "Probability of false positives")
plt.title('Probability of false positives')
plt.xlabel('Words Counts')
plt.ylabel('False Positive Rate')
plt.legend()


      

