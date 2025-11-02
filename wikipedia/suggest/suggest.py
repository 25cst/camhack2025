from collections import deque
import readdb

def get_nodes_at_dist_lazy(source, dist):
    source = readdb.title_to_id[source]
    q: deque[tuple[int, int]] = deque()
    q.append((source, 0))

    visited = {source}
    yield_queue: deque[int] = deque()
    prev_nodes = {}

    while len(q) != 0:
        (node, d) = q.popleft()
        if d == dist:
            yield_queue.append(node)
            continue

        for neighbour in readdb.relations[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                prev_nodes[neighbour] = node
                q.append((neighbour, d + 1))

    while len(yield_queue) != 0:
        node = yield_queue.popleft()
        yield readdb.id_to_title[node]
        if node != source:
            yield_queue.append(prev_nodes[node])

def get_multiple_paths_lazy(source, dest):
    source = readdb.title_to_id[source]
    dest = readdb.title_to_id[dest]
    q: deque[int] = deque()
    q.append(source)

    visited = {source}
    prev_nodes = {}

    while len(q) != 0:
        node = q.popleft()

        for neighbour in readdb.relations[node]:
            if neighbour not in visited and neighbour != dest:
                visited.add(neighbour)
                prev_nodes[neighbour] = node
                q.append(neighbour)

            elif neighbour == dest:
                visited.add(neighbour)
                prev_nodes[neighbour] = node
                p = []
                node_copy = neighbour
                while node_copy != source:
                    p.append(readdb.id_to_title[node_copy])
                    node_copy = prev_nodes[node_copy]
                p.append(readdb.id_to_title[source])
                yield p[::-1]

def get_nodes_bfs_lazy(source):
    source = readdb.title_to_id[source]
    q: deque[int] = deque()
    q.append(source)

    visited = {source}

    while len(q) != 0:
        node = q.popleft()
        if node != source:
            yield node

        for neighbour in readdb.relations[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                q.append(neighbour)

def get_hints(guess, secret, n, hint_level):
    hints = set()
    guess_dist = -1
    for hint_path in get_multiple_paths_lazy(guess, secret):
        hint_length = len(hint_path)
        if guess_dist == -1:
            # Get the closest distance between guess and secret, used later to get other hints at the same distance
            guess_dist = hint_length - 1

        # Either the secret is the next word after guess, or the guess is spot on
        if hint_length <= 2:
            continue

        hints.add(hint_path[-min(guess_dist - hint_level + 1, guess_dist)])
        if len(hints) == n:
            return hints

    for hint in get_nodes_at_dist_lazy(secret, max((guess_dist - hint_level if guess_dist >= 0 else hint_level), 1)):
        if hint != guess and hint != secret and hint not in hints:
            hints.add(hint)

        if len(hints) == n:
            return hints

    # this is just in case the other two approaches don't find enough hints - searches for any nodes that are not yet in hints
    for hint in get_nodes_bfs_lazy(secret):
        if hint != guess and hint != secret and hint not in hints:
            hints.add(hint)

        if len(hints) == n:
            return hints

    # if no path found, set the distance to a big number so that closeness is 0
    if guess_dist == -1:
        guess_dist = 100

    return hints, int(max(100 * (6 - guess_dist) / 6, 0))
