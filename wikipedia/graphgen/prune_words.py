import random

id_to_title: dict[int, str] = {}
title_to_id: dict[str, int] = {}

_relations_sets: dict[int, set[int]] = dict()
relations: dict[int, list[int]] = dict()

print("Reading cache.txt")
def connect_nodes(a, b):
    _relations_sets[a].add(b)
    # if random.uniform(0, 1) < 0.1:
    # _relations_sets[b].add(a)

with open("../graphgen/cache.txt", "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        title = line.split("|")[0].strip()
        if len(line.split("|")) <= 10 + 1:
            continue
        id_to_title[i] = title
        title_to_id[title] = i
        _relations_sets[i] = set()
    print(len(_relations_sets))

    for line in lines:
        chunks = line.split('|')
        if chunks[0].strip() not in title_to_id:
            continue
        title_id = title_to_id[chunks[0].strip()]
        for chunk in chunks[1:]:
            if chunk.strip() not in title_to_id:
                continue
            neighbour_id = title_to_id[chunk.strip()]
            connect_nodes(title_id, neighbour_id)

    for title_id in _relations_sets.keys():
        relations[title_id] = sorted(_relations_sets[title_id], key=lambda x: len(_relations_sets[x]), reverse=True)
print("Done reading cache.txt")
print(len(list(filter(lambda x: len(relations[x]) <= 10, relations.keys()))))

entryLines = []

for title in relations.keys():
    neighbours = relations[title]
    entries = [id_to_title[title], *list(map(lambda x: id_to_title[x], neighbours))]
    entryLines.append("|".join(entries))

with open("cache.txt", "w") as f:
    f.write("\n".join(entryLines))