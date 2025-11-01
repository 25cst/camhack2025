from libzim.reader import Archive
from pathlib import Path
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

parser = etree.HTMLParser()

zim = Archive(Path("/home/siriusmart/.local/share/kiwix/wikipedia_en_top_nopic_2025-09.zim"))
relations: dict[str, set[str]] = dict()

c = 0

allowed = set()

def isAllowed(s):
    for c in s:
        if not c.isalnum() or c == '_' or c == '-':
            return False
    return True

for i in range(zim.all_entry_count):
    entry = zim._get_entry_by_id(i)
    if isAllowed(entry.title):
        allowed.add(entry.title)

c = 0

def push(entry):
    global c
    c += 1
    if c % 100 == 0:
        print(f"{c} of {zim.all_entry_count}")
        try:

            if not entry.title in allowed:
                return

            root = etree.fromstring(bytes(entry.get_item().content).decode("UTF-8"), parser)

            outlinks = set()

            for a in root.xpath("//a"):
                href: str = a.get('href')
                if href == None:
                    continue
                href = href.split("#")[0]
                if zim.has_entry_by_title(href):
                    outlinks.add(href)


            relations[entry.title] = outlinks
        except:
            pass

values = []

for i in range(zim.all_entry_count):
    entry = zim._get_entry_by_id(i)
    values.append(entry)

with ThreadPoolExecutor(max_workers=16) as exe:
    exe.map(push, values)

print("done parsing, writing to db")
