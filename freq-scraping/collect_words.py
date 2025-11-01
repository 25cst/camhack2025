#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re
import time

TRIPLE_RE = re.compile(r"^(\d{4}),(\d+),(\d+)$")  # year,match,vol


def load_words(path: str, lowercase=True) -> Set[str]:
    print(f"🔤 Loading target words from {path} ...")
    out = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if not w or w.startswith("#"):
                continue
            out.add(w.lower() if lowercase else w)
    print(f"✅ Loaded {len(out):,} words to search for.")
    return out


def parse_line(parts: List[str]) -> List[Tuple[int, int, int]]:
    """Parses a single Ngram line into (year, match, volume) tuples."""
    triples = []
    if len(parts) == 4 and parts[1].isdigit():
        # classic format: token \t year \t match \t vol
        return [(int(parts[1]), int(parts[2]), int(parts[3]))]

    for field in parts[1:]:
        field = field.strip()
        if not field:
            continue
        m = TRIPLE_RE.match(field)
        if m:
            triples.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
        else:
            for sub in field.split():
                m2 = TRIPLE_RE.match(sub)
                if m2:
                    triples.append(
                        (int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
                    )
    return triples


def walk_files(input_dir: str, glob_pattern: str) -> List[Path]:
    print(f"📁 Searching for files in {input_dir} matching '{glob_pattern}' ...")
    paths = sorted(Path(input_dir).glob(glob_pattern))
    print(f"✅ Found {len(paths)} files.")
    return paths


def collect_aggregated(
    files: List[Path],
    wanted_words: Set[str],
    include_untagged: bool,
    case_sensitive: bool,
    min_year: int,
    max_year: int,
    keep_pos: bool,
):
    agg: Dict[Tuple[str, int], Tuple[int, int]] = {}
    pos_split: Dict[Tuple[str, str, int], Tuple[int, int]] = {} if keep_pos else None

    print(f"🚀 Starting collection across {len(files)} files ...")
    start_time = time.time()
    total_lines = 0
    matched_lines = 0

    for idx, fp in enumerate(files, 1):
        print(f"📄 Processing file {idx}/{len(files)}: {fp.name}")
        line_count = 0
        file_matches = 0

        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            for raw in f:
                total_lines += 1
                line_count += 1
                if not raw or raw == "\n":
                    continue

                parts = raw.rstrip("\n").split("\t")
                token = parts[0]
                if "_" in token:
                    base, pos = token.rsplit("_", 1)
                else:
                    base, pos = token, "UNTAGGED"

                base_key = base if case_sensitive else base.lower()
                if base_key not in wanted_words:
                    continue

                if pos == "UNTAGGED" and not include_untagged and "_" not in token:
                    continue

                triples = parse_line(parts)
                if not triples:
                    continue

                file_matches += 1
                matched_lines += 1

                for (y, m, v) in triples:
                    if (min_year and y < min_year) or (max_year and y > max_year):
                        continue

                    # aggregate across POS
                    k = (base_key, y)
                    pm, pv = agg.get(k, (0, 0))
                    agg[k] = (pm + m, pv + v)

                    if keep_pos:
                        kp = (base_key, pos, y)
                        pm2, pv2 = pos_split.get(kp, (0, 0))
                        pos_split[kp] = (pm2 + m, pv2 + v)

        print(f"   ↳ Processed {line_count:,} lines, found {file_matches:,} matches.")

    elapsed = time.time() - start_time
    print(
        f"✅ Done scanning all files. "
        f"Processed {total_lines:,} lines, found {matched_lines:,} matching entries "
        f"in {elapsed:.1f}s."
    )
    return agg, pos_split


def write_agg(path: str, agg: Dict[Tuple[str, int], Tuple[int, int]]):
    print(f"💾 Writing aggregated results to {path} ...")
    with open(path, "w", encoding="utf-8") as w:
        w.write("word\tyear\tmatch_count\tvolume_count\n")
        for (word, year) in sorted(agg.keys(), key=lambda k: (k[0], k[1])):
            m, v = agg[(word, year)]
            w.write(f"{word}\t{year}\t{m}\t{v}\n")
    print(f"✅ Wrote {len(agg):,} aggregated rows.")


def write_pos(path: str, pos_split: Dict[Tuple[str, str, int], Tuple[int, int]]):
    print(f"💾 Writing POS-split results to {path} ...")
    with open(path, "w", encoding="utf-8") as w:
        w.write("word\tpos\tyear\tmatch_count\tvolume_count\n")
        for (word, pos, year) in sorted(pos_split.keys(), key=lambda k: (k[0], k[1], k[2])):
            m, v = pos_split[(word, pos, year)]
            w.write(f"{word}\t{pos}\t{year}\t{m}\t{v}\n")
    print(f"✅ Wrote {len(pos_split):,} POS-split rows.")


def main():
    ap = argparse.ArgumentParser(
        description="Collect per-year frequencies for a word list, aggregating across POS (NOUN/ADJ/etc.)."
    )
    ap.add_argument("--input-dir", required=True, help="Folder with unzipped 1-gram files")
    ap.add_argument("--glob", default="googlebooks-eng-all-1gram-20120701-*",
                    help="Glob to match files (default: all a–z parts)")
    ap.add_argument("--words", required=True, help="Text file: one target word per line")
    ap.add_argument("--include-untagged", action="store_true",
                    help="Also include bare tokens without POS suffix if present")
    ap.add_argument("--case-sensitive", action="store_true",
                    help="Match words case-sensitively (default: case-insensitive)")
    ap.add_argument("--min-year", type=int, default=0, help="Minimum year to keep (inclusive)")
    ap.add_argument("--max-year", type=int, default=0, help="Maximum year to keep (inclusive; 0 = no cap)")
    ap.add_argument("-o", "--output", required=True, help="Output TSV path (POS-aggregated)")
    ap.add_argument("--keep-pos", action="store_true",
                    help="Also write a POS-split TSV alongside the aggregated one")
    ap.add_argument("--pos-output", default="", help="Path for POS-split TSV (required if --keep-pos)")
    args = ap.parse_args()

    wanted = load_words(args.words, lowercase=(not args.case_sensitive))
    files = walk_files(args.input_dir, args.glob)
    if not files:
        raise SystemExit(f"No files matched {args.input_dir}/{args.glob}")

    agg, pos_split = collect_aggregated(
        files=files,
        wanted_words=wanted,
        include_untagged=args.include_untagged,
        case_sensitive=args.case_sensitive,
        min_year=args.min_year,
        max_year=args.max_year,
        keep_pos=args.keep_pos,
    )

    write_agg(args.output, agg)
    if args.keep_pos:
        if not args.pos_output:
            raise SystemExit("--pos-output is required when --keep-pos is set")
        write_pos(args.pos_output, pos_split)


if __name__ == "__main__":
    main()
