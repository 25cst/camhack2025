import suggest
import readdb
from time import perf_counter
import random

entries = list(readdb.relations.keys())

print("done loading")

def test():
    src = random.choice(entries)
    dest = random.choice(entries)
    print("doing",readdb.id_to_title[src], readdb.id_to_title[dest])

    # src = readdb.title_to_id["Apocynthion"]
    # dest = readdb.title_to_id["AC-DC"]

    start = perf_counter()
    # print(list(suggest.get_multiple_paths_lazy(readdb.id_to_title[src], readdb.id_to_title[dest])))
    print(s := suggest.get_hints(readdb.id_to_title[src], readdb.id_to_title[dest], 5, 1))
    if len(s) == 0:
        print("couldn't find", readdb.id_to_title[src], readdb.id_to_title[dest])
    end = perf_counter()

    assert len(s) == 5

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
