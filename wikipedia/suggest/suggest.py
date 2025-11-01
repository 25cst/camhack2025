from collections import deque
import readdb
import copy

def path(source, dest):
    q: deque[tuple[list[str], str]] = deque()
    q.append(([], source))

    visited = set()

    while len(q) != 0:
        (path, node) = q.popleft()
        
        if node in visited:
            continue

        path.append(node)

        if node == dest:
            return path

        for neighbour in readdb.relations[node]:
            if not neighbour in visited:
                q.append((copy.deepcopy(path), neighbour))
