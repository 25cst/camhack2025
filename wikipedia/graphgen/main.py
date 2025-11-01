from libzim.reader import Archive
from pathlib import Path
from html.parser import HTMLParser

import os

zim = Archive(Path("/home/siriusmart/.local/share/kiwix/wikipedia_en_top_nopic_2025-09.zim"))
entry = zim.get_entry_by_path("index")

relations: dict[str, set[str]] = dict()

for i in range(zim.all_entry_count):
    title = zim._get_entry_by_id(i).title

    outlinks = set()

    relations[title]

    print()
