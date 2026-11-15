
from pathlib import Path
from collections import Counter
import re

PROJECT_DIR = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_DIR.parent / "datasets" / "text-files"
OUTPUT_DIR = PROJECT_DIR / "output_results"

# Independent word count using Python Counter
direct_counts = Counter()

input_files = sorted(DATASET_DIR.glob("book_*.txt"))

for file_path in input_files:
    text = file_path.read_text(encoding="utf-8")
    words = re.findall(r"[a-zA-Z]+", text.lower())
    direct_counts.update(words)

# Read MapReduce output
mapreduce_counts = {}

output_files = sorted(OUTPUT_DIR.glob("part-*"))

for file_path in output_files:
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        word, count = line.split()

        if word in mapreduce_counts:
            raise ValueError(f"Duplicate output word: {word}")

        mapreduce_counts[word] = int(count)

# Compare results
print("=" * 50)
print("INDEPENDENT WORD COUNT VALIDATION")
print("=" * 50)

print(f"Input files: {len(input_files)}")
print(f"Counter unique words: {len(direct_counts)}")
print(f"MapReduce unique words: {len(mapreduce_counts)}")

print(f"\nCounter total words: {sum(direct_counts.values())}")
print(f"MapReduce total words: {sum(mapreduce_counts.values())}")

if dict(direct_counts) == mapreduce_counts:
    print("\nVALIDATION: PASSED")
    print("MapReduce matches Python Counter exactly!")
else:
    print("\nVALIDATION: FAILED")

    for word in sorted(set(direct_counts) | set(mapreduce_counts)):
        expected = direct_counts.get(word, 0)
        actual = mapreduce_counts.get(word, 0)

        if expected != actual:
            print(f"{word}: Counter={expected}, MapReduce={actual}")
