import gzip
import shutil
import os

in_dir = "ngrams-new"

for filename in os.listdir(in_dir):
    if filename.endswith(".gz"):
        gz_path = os.path.join(in_dir, filename)
        out_path = os.path.join(in_dir, filename[:-3])  # remove .gz
        print(f"🗜️ Unzipping {filename} ...")
        with gzip.open(gz_path, "rb") as f_in, open(out_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

print("✅ All files unzipped!")
