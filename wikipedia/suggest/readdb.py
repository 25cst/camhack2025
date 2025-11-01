import sqlite3

con = sqlite3.connect("./relations.sqlite")
cur = con.cursor()
cur.execute("SELECT * FROM relations")

entries = cur.fetchall()

relations: dict[str, set[str]] = dict()

for [source, dest] in entries:
    if not source in relations:
        relations[source] = set()

    relations[source].add(dest)
