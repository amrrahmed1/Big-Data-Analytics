# Parallel MapReduce Word Count

## Project Overview

This project implements a MapReduce Word Count system using Python, demonstrating the five main MapReduce phases and parallel processing.

## Dataset

The project uses five text files provided in `datasets/text-files/`.

- book_01.txt
- book_02.txt
- book_03.txt
- book_04.txt
- book_05.txt

## Implementation

The system implements the following phases:

1. **Map:** Extract words and generate (word, 1) pairs.
2. **Combine:** Aggregate word counts locally for each file.
3. **Partition:** Distribute intermediate pairs between two reducers.
4. **Shuffle & Sort:** Group values by word and sort the keys.
5. **Reduce:** Calculate final word frequencies.

Parallel processing is implemented using Python's `ProcessPoolExecutor` with four mapper workers.

## How to Run

Run these commands from the repository root:

```bash
py MapReduce-Bonus/mapreduce_sim.py
py MapReduce-Bonus/validate_output.py
```

The first command executes MapReduce and saves the results in `MapReduce-Bonus/output_results/`.

The second command compares MapReduce results against an independent Python Counter implementation.

## Results

| Metric | Result |
|---|---|
| Input Files | 5 |
| Parallel Workers | 4 |
| Reducers | 2 |
| Total Mapped Pairs | 235 |
| Total Combined Pairs | 215 |
| Unique Words | 182 |
| Total Word Occurrences | 235 |

## Validation

Independent validation using Python Counter passed, confirming that the MapReduce output matches direct counting with the same tokenization rules.

The supplied `expected_word_count.txt` does not fully match the generated counts and contains a duplicate `reduce` key. This discrepancy remains unresolved.

## Requirements

- Python 3.11+
- Python standard library only
- No external dependencies required
