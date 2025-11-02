import re
from collections import deque
from sentence_transformers import SentenceTransformer
import readdb

print("Loading transformer model")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Done loading model")

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

def get_closeness(w1, w2):
    emb = model.encode([w1, w2])
    return int(model.similarity(emb, emb)[0, 1].item() * 100)

def get_hints(guess, secret, n, hint_level):
    used_words = {guess, secret}
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

        hint = hint_path[-max(min(guess_dist - hint_level + 1, guess_dist), 2)]

        hints.add((hint, get_closeness(hint, secret)))
        used_words.add(hint)

        if len(hints) == n:
            return hints, get_closeness(guess, secret)

    for hint in get_nodes_at_dist_lazy(secret, max((guess_dist - hint_level if guess_dist >= 0 else hint_level), 1)):
        if hint not in used_words:
            hints.add((hint, get_closeness(hint, secret)))
            used_words.add(hint)

        if len(hints) == n:
            return hints, get_closeness(guess, secret)

    # this is just in case the other two approaches don't find enough hints - searches for any nodes that are not yet in hints
    for hint in get_nodes_bfs_lazy(secret):
        if hint not in used_words:
            hints.add((hint, get_closeness(hint, secret)))
            used_words.add(hint)

        if len(hints) == n:
            return hints, get_closeness(guess, secret)

    # if no path found, set the distance to a big number so that closeness is 0
    # if guess_dist == -1:
    #     guess_dist = 100

    return hints, get_closeness(guess, secret)

def get_possible_words(frag, n):
    return list(filter(lambda x: x[:len(frag)].lower() == frag.lower(), readdb.title_to_id.keys()))[:n]
