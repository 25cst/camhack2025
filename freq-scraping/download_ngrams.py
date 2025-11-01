import os
import string
import subprocess

base_url = "http://storage.googleapis.com/books/ngrams/books/20200217/eng/"
out_dir = "ngrams-new"
os.makedirs(out_dir, exist_ok=True)

for i in range(7, 24):
    if i < 10:
        i = '0' + str(i)
    url = f"{base_url}1-000{i}-of-00024.gz"
    print(f"Downloading {url}...")
    subprocess.run(["wget", "-c", "-P", out_dir, url])

print("✅ All downloads complete! Files saved in", out_dir)
