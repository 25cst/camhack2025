import suggest
import readdb
from time import perf_counter
import random

entries = list(readdb.relations.keys())

def test():
    src = random.choice(entries)
    dest = random.choice(entries)

    start = perf_counter()
    print(suggest.path(src, dest))
    end = perf_counter()

    return end - start

m = 0
avg = 0
T = 100000
for _ in range(T):
    t = test()
    if t > m:
        m = t
        print("new max time:", m)
    avg += t

avg /= T
print("avg time:", avg)
