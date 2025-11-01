from libzim.reader import Archive
from pathlib import Path
from html.parser import HTMLParser

import os

zim = Archive(Path("/home/siriusmart/.local/share/kiwix/wikipedia_en_top_nopic_2025-09.zim"))
relations: dict[str, set[str]] = dict()

for i in range(zim.all_entry_count):
    entry = zim._get_entry_by_id(i)
    parser = HTMLParser()
    parser.feed(bytes(entry.get_item().content).decode("UTF-8"))

    break

    outlinks = set()

    relations[entry.title]

    print()
