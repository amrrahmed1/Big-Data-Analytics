
from pathlib import Path
import re

# Dataset path
DATASET_DIR = Path(__file__).resolve().parent.parent / "datasets" / "text-files"


# Phase 1: MAP
def mapper(file_path):
    text = file_path.read_text(encoding="utf-8")

    # Convert text into lowercase words
    words = re.findall(r"[a-zA-Z]+", text.lower())

    # Emit (word, 1) for each word
    return [(word, 1) for word in words]


def main():
    input_files = sorted(DATASET_DIR.glob("book_*.txt"))

    if not input_files:
        raise FileNotFoundError("No input text files found!")

    mapped_results = []

    for file_path in input_files:
        pairs = mapper(file_path)
        mapped_results.extend(pairs)

        print(f"{file_path.name}: {len(pairs)} words mapped")

    print("\nTotal mapped pairs:", len(mapped_results))
    print("\nFirst 10 mapped pairs:")
    print(mapped_results[:10])


if __name__ == "__main__":
    main()
