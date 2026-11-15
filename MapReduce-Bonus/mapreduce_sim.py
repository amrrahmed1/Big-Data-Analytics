
from pathlib import Path
import re

# Dataset path
DATASET_DIR = Path(__file__).resolve().parent.parent / "datasets" / "text-files"


# Phase 1: MAP
def mapper(file_path):
    text = file_path.read_text(encoding="utf-8")
    words = re.findall(r"[a-zA-Z]+", text.lower())

    return [(word, 1) for word in words]


# Phase 2: COMBINE
def combiner(mapped_pairs):
    word_counts = {}

    for word, count in mapped_pairs:
        word_counts[word] = word_counts.get(word, 0) + count

    return list(word_counts.items())


def main():
    input_files = sorted(DATASET_DIR.glob("book_*.txt"))

    if not input_files:
        raise FileNotFoundError("No input text files found!")

    combined_results = []
    total_mapped = 0

    for file_path in input_files:
        # Map phase
        mapped_pairs = mapper(file_path)

        # Combine phase (locally per file)
        combined_pairs = combiner(mapped_pairs)

        combined_results.extend(combined_pairs)
        total_mapped += len(mapped_pairs)

        print(f"\nFile: {file_path.name}")
        print(f"Mapped pairs: {len(mapped_pairs)}")
        print(f"Combined pairs: {len(combined_pairs)}")

    print("\n" + "-" * 45)
    print("MAP + COMBINE SUMMARY")
    print("-" * 45)

    print("Total mapped pairs:", total_mapped)
    print("Total combined pairs:", len(combined_results))

    print("\nFirst 10 combined pairs:")
    for pair in combined_results[:10]:
        print(pair)


if __name__ == "__main__":
    main()
