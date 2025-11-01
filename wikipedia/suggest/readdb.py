import sqlite3

con = sqlite3.connect("./relations.sqlite")
cur = con.cursor()
entries = cur.execute("SELECT * FROM relations;").fetchall()

relations: dict[str, set[str]] = dict()

for (source, dest) in entries:
    if not source in relations:
        relations[source] = set()

    relations[source].add(dest)
