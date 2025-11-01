id_to_title: dict[int, str] = {}
title_to_id: dict[str, int] = {}

relations: dict[int, set[int]] = dict()

with open("../graphgen/cache.txt", "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        title = line.split("|")[0].strip()
        id_to_title[i] = title
        title_to_id[title] = i
    for line in lines:
        chunks = line.split('|')
        relations[title_to_id[chunks[0].strip()]] = set(map(lambda x: title_to_id[x.strip()], chunks[1:]))
