from collections import deque
import readdb

def path(source, dest):
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
                p.append(readdb.id_to_title[node])
                node = prev_nodes[node]
            p.append(readdb.id_to_title[source])
            return p[::-1]

        for neighbour in readdb.relations[node]:
            if not neighbour in visited:
                visited.add(neighbour)
                q.append((node, neighbour))
