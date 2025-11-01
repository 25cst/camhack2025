from libzim.reader import Archive
from pathlib import Path
from lxml import etree

parser = etree.HTMLParser()

zim = Archive(Path("/home/siriusmart/.local/share/kiwix/wikipedia_en_top_nopic_2025-09.zim"))
relations: dict[str, set[str]] = dict()


c = 0

for i in range(zim.all_entry_count):
    entry = zim._get_entry_by_id(i)
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

    c += 1

    if c % 100 == 0:
        print(c)
