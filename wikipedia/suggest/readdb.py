relations: dict[str, set[str]] = dict()

for line in open("../graphgen/cache.txt", "r").read().split("\n"):
    chunks = line.split('|')
    relations[chunks[0]] = set(chunks[1:])
