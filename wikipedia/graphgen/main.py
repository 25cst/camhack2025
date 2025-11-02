from libzim.reader import Archive
from pathlib import Path
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import sqlite3

parser = etree.HTMLParser()

# zim = Archive(Path("/home/siriusmart/.local/share/kiwix/wikipedia_en_top_nopic_2025-09.zim"))
zim = Archive(Path("/home/chris/Downloads/wiki temp/wikipedia_en_top_nopic_2025-09.zim"))
relations: dict[str, set[str]] = dict()

c = 0

allowed = set()

def isAllowed(s):
    if s == "index": return False
    for c in s:
        if not (c.isalnum() or c == '_' or c == '-') or not c.isascii():
            return False
    return True

for i in range(zim.all_entry_count):
    entry = zim._get_entry_by_id(i)
    if isAllowed(entry.title) and zim.has_entry_by_title(entry.title):
        allowed.add(entry.title)

print(len(allowed))

values = set()

c = 0

def push(entry):
    global c, relations, allowed
    c += 1
    if c % 100 == 0:
        print(f"{c} of {len(values)}")

    root = etree.fromstring(bytes(entry.get_item().content).decode("UTF-8"), parser)

    outlinks = set()

    for a in root.xpath("//a"):
        href: str = a.get('href')
        if href == None:
            continue
        href = href.split("#")[0]
        if href not in allowed:
            continue
        if zim.has_entry_by_title(href):
            outlinks.add(href)
    relations[entry.title] = outlinks

for title in allowed:
    # print(title)
    entry = zim.get_entry_by_title(title)
    values.add(entry)

with ThreadPoolExecutor(max_workers=16) as exe:
    exe.map(push, values)

print("done parsing, writing to db")
print(len(relations))

entryLines = []

for title in allowed:
    neighbours = relations[title]
    entries = [title, *neighbours]
    entryLines.append("|".join(entries))

with open("cache.txt", "w") as f:
    f.write("\n".join(entryLines))
