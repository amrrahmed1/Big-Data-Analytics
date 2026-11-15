
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import re

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "datasets" / "text-files"
OUTPUT_DIR = Path(__file__).resolve().parent / "output_results"


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


# Phase 3: PARTITION
def partitioner(combined_pairs):
    partitions = {
        0: [],
        1: []
    }

    for word, count in combined_pairs:
        if word[0] <= "m":
            partitions[0].append((word, count))
        else:
            partitions[1].append((word, count))

    return partitions


# Phase 4: SHUFFLE & SORT
def shuffle_and_sort(partitions):
    shuffled_data = {}

    for reducer_id, pairs in partitions.items():
        grouped = defaultdict(list)

        for word, count in pairs:
            grouped[word].append(count)

        shuffled_data[reducer_id] = dict(
            sorted(grouped.items())
        )

    return shuffled_data


# Phase 5: REDUCE
def reducer(grouped_data):
    final_counts = {}

    for word, counts in grouped_data.items():
        final_counts[word] = sum(counts)

    return final_counts


# Parallel Mapper Worker
def process_file(file_path):
    mapped_pairs = mapper(file_path)
    combined_pairs = combiner(mapped_pairs)

    return file_path.name, len(mapped_pairs), combined_pairs


def main():
    input_files = sorted(DATASET_DIR.glob("book_*.txt"))

    if not input_files:
        raise FileNotFoundError("No input text files found!")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_combined_pairs = []
    total_mapped = 0

    print("=" * 50)
    print("PARALLEL MAPREDUCE WORD COUNT PROJECT")
    print("=" * 50)

    # PARALLEL MAP + COMBINE
    num_workers = min(4, len(input_files))

    print(f"\nRunning {num_workers} parallel mapper workers...")

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(process_file, input_files)

        for file_name, mapped_count, combined_pairs in results:
            all_combined_pairs.extend(combined_pairs)
            total_mapped += mapped_count

            print(f"\nFile: {file_name}")
            print(f"Mapped pairs: {mapped_count}")
            print(f"Combined pairs: {len(combined_pairs)}")

    # PARTITION
    partitions = partitioner(all_combined_pairs)

    print("\n" + "=" * 50)
    print("PARTITION RESULTS")
    print("=" * 50)

    for reducer_id, pairs in partitions.items():
        print(f"Reducer {reducer_id + 1}: {len(pairs)} pairs")

    # SHUFFLE & SORT
    shuffled_data = shuffle_and_sort(partitions)

    print("\n" + "=" * 50)
    print("SHUFFLE & SORT RESULTS")
    print("=" * 50)

    for reducer_id, grouped in shuffled_data.items():
        print(
            f"Reducer {reducer_id + 1}: "
            f"{len(grouped)} unique words"
        )

    # REDUCE
    all_results = {}

    print("\n" + "=" * 50)
    print("REDUCE RESULTS")
    print("=" * 50)

    for reducer_id, grouped in shuffled_data.items():
        reduced_counts = reducer(grouped)

        all_results.update(reduced_counts)

        output_file = OUTPUT_DIR / f"part-{reducer_id:05d}"

        with output_file.open("w", encoding="utf-8") as f:
            for word, count in reduced_counts.items():
                f.write(f"{word} {count}\n")

        print(f"\nReducer {reducer_id + 1}")
        print(f"Unique words: {len(reduced_counts)}")
        print(f"Saved to: {output_file.name}")

    # FINAL SUMMARY
    print("\n" + "=" * 50)
    print("FINAL MAPREDUCE SUMMARY")
    print("=" * 50)

    print(f"Input files: {len(input_files)}")
    print(f"Total mapped pairs: {total_mapped}")
    print(f"Total combined pairs: {len(all_combined_pairs)}")
    print(f"Total unique words: {len(all_results)}")
    print(f"Total word occurrences: {sum(all_results.values())}")

    # Verify no words were lost
    assert sum(all_results.values()) == total_mapped

    print("\nWord count consistency check: PASSED")

    print("\nTop 10 Most Frequent Words:")
    top_words = sorted(
        all_results.items(),
        key=lambda item: (-item[1], item[0])
    )[:10]

    for word, count in top_words:
        print(f"{word}: {count}")

    print("\nMapReduce execution completed successfully!")


if __name__ == "__main__":
    main()