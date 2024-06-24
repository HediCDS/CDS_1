#import necessary packages
from Bloom_filter import BloomFilter
import random
import time
import string
import matplotlib.pyplot as plt
import typing
import numpy as np

#Function to provide lowercase strings of given length
def get_words(ln: int) -> str:
    charachters = string.ascii_lowercase
    return "".join(random.choice(charachters) for _ in range(ln))
    
#Function to provide strings that are unique from the inserted ones, this to test false positives
def list_words(exp_count: int, words, min=3, max=12):
    wlist = set()
    while len(wlist) < exp_count:
        string = get_words(random.randint(min, max))
        if string not in words:
            wlist.add(string)
    return list(wlist)

#Function to provide insertion times, search times and probabilities of false positives
def benchmark(nlist, p):
    time_insert = []
    time_search = []
    prob_fpos = []
    comp_rates = []
    for n in nlist:
        #create a bloom filter
        bf = BloomFilter(n, p)
        
        #get strings to be inserted
        strings_inserted = list_words(n, set())
        
        #mark the current time
        begin_time = time.time()
        
        #insert strings
        for string in strings_inserted:
            bf.insert(string)
            
        #mark insertion time
        time_ins = time.time() - begin_time
        
        #add the time to the insertion time list
        time_insert.append(time_ins)

        #Provide a list og inserted and not inserted words
        strings_check_list = strings_inserted[:n // 2] + list_words(n // 2, set(strings_inserted)) 

        #mark the time
        begin_search_time = time.time()

        #set false positives counter to 0
        fp = 0
        for s in strings_check_list:
            #search and track the fpositives
            if bf.search(s) and s not in strings_inserted:
                fp += 1
        #mark the search time and append to search time list
        check_time = time.time() - begin_search_time
        time_search.append(check_time)  

        #Calculate the fp rate and append to the list of fp rates
        fprate = fp / (n // 2)
        prob_fpos.append(fprate)

        #compute the compression rate
        true_size = bf.size
        approp_size = -(n * np.log(p)) / (np.log(2) ** 2)
        comp_rate = approp_size / true_size
        comp_rates.append(comp_rate)
        
    return time_insert, time_search, prob_fpos, comp_rates

#Test with large samples and expected false pos rate
nlist = [1000, 5000, 10000, 50000, 100000]
fprate = 0.05

#call the benchmark
time_insert, time_search, prob_fp, comp_rates = benchmark(nlist, fprate)


plt.figure(figsize=(14, 8))

#plot the insertion time
plt.subplot(1, 3, 1)
plt.plot(nlist, time_insert, label = "Insertion Time")
plt.xlabel('Words Counts')
plt.ylabel('Time in seconds')
plt.legend()

#plot seach time

plt.subplot(1, 3, 2)
plt.plot(nlist, time_search, label = "Search Time")
plt.title('Search Time')
plt.xlabel('Words Counts')
plt.ylabel('Time in seconds')
plt.legend()

#plot fp probability
plt.subplot(1, 3, 3)
plt.plot(nlist, prob_fp, label = "Probability of false positives")
plt.title('Probability of false positives')
plt.xlabel('Words Counts')
plt.ylabel('False Positive Rate')
plt.legend()
plt.savefig('benchmark_results.png')


plt.figure(figsize=(12, 8))

#plot the compression rate
plt.plot(nlist, comp_rates, label = "Compression rate")
plt.xlabel('Words Counts')
plt.ylabel('Compression Rate')
plt.legend()
plt.savefig('Compression_rates.png')

