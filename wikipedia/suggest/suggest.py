from collections import deque
import random
import readdb

def randomWalk(origin, distance):
    origin = readdb.title_to_id[origin]
    walked = []

    while distance != 0:
        walked.append(origin)
        neighbours = list(filter((lambda n : not n in walked), readdb.relations[origin]))

        if len(neighbours) == 0:
            if len(walked) == 0:
                return None
            else:
                return readdb.id_to_title[origin]

        origin = random.choice(neighbours)
        walked.append(origin)
        distance -= 1

    return readdb.id_to_title[origin]

def path(source, dest):
    source = readdb.title_to_id[source]
    dest = readdb.title_to_id[dest]
    q: deque[tuple[int, int]] = deque()
    q.append((source, source))

    visited = {source}
    prev_nodes = {}

    while len(q) != 0:
        (prev, node) = q.popleft()
        prev_nodes[node] = prev

        if node == dest:
            p = []
            while node != source:
                p.append(node)
                node = prev_nodes[node]
            p.append(source)
            return list(map((lambda x : readdb.id_to_title[x]), p[::-1]))

        for neighbour in readdb.relations[node]:
            if not neighbour in visited:
                visited.add(neighbour)
                q.append((node, neighbour))

print(randomWalk("Physics", 1))
