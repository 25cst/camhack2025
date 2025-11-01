from collections import deque
import readdb

def path(source, dest):
    q = deque()
    q.append(([], source))

    visited = set()

    while len(q) != 0:
        (path, node) = q.popleft()
        
        if node in visited:
            continue

        if node == dest:
            path.append(node)
            return path

        for neighbour in readdb.relations[node]:
            if not neighbour in visited:
                q.append(neighbour)
