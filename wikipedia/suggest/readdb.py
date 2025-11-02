import random

id_to_title: dict[int, str] = {}
title_to_id: dict[str, int] = {}

_relations_sets: dict[int, set[int]] = dict()
relations: dict[int, list[int]] = dict()

print("Reading cache.txt")
def connect_nodes(a, b):
    _relations_sets[a].add(b)
    if random.uniform(0, 1) < 0.1:
        _relations_sets[b].add(a)

with open("../graphgen/cache.txt", "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        title = line.split("|")[0].strip()
        id_to_title[i] = title
        title_to_id[title] = i
        _relations_sets[i] = set()

    for line in lines:
        chunks = line.split('|')
        title_id = title_to_id[chunks[0].strip()]
        for chunk in chunks[1:]:
            neighbour_id = title_to_id[chunk.strip()]
            connect_nodes(title_id, neighbour_id)

print("Done reading cache.txt")
