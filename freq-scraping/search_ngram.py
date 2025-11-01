import sys
import os

def search_ngram(input_file: str, search_word: str, output_file: str):
    """
    Search for lines that start with a given word in a large Ngram file
    and write them to a separate file.
    """
    # Normalize search word to match exact ngram (case-sensitive)
    # You can lower() both if you want case-insensitive
    matches = 0
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", encoding="utf-8") as outfile:
        for line in infile:
            # Each line starts with the ngram, then a tab or space
            if line.startswith(search_word + "\t") or line.startswith(search_word + " "):
                outfile.write(line)
                matches += 1

    print(f"✅ Done! Found {matches} matching lines.")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 search_ngram.py <input_file> <word> <output_file>")
        sys.exit(1)

    input_path = sys.argv[1]
    word = sys.argv[2]
    output_path = sys.argv[3]

    if not os.path.exists(input_path):
        print(f"Error: input file '{input_path}' not found.")
        sys.exit(1)

    search_ngram(input_path, word, output_path)
