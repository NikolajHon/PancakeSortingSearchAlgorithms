# README.md

## Pancake Sorting Problem Solver

This repository provides an implementation of various search algorithms to solve the Pancake Sorting Problem. The goal of the problem is to sort a stack of sticks using the minimum number of flips, where a flip reverses the order of a prefix of the stack.

### Features

- **Uniform Cost Search (UCS)**
- **A* Search** with multiple heuristic functions:
  - Largest Misplaced Stick
  - Sum of Distances to the Goal
  - Gap Heuristic
  - Weighted Gap Heuristic
- **Greedy Search** with the same heuristic functions as A*

### Requirements

- Python 3.6+

### Installation

No additional libraries are required, as the implementation uses Python's standard library. Clone the repository and navigate to the folder:

```bash
$ git clone https://github.com/your-repo/pancake-sorting
$ cd pancake-sorting
```

### Usage

Run the script using:

```bash
$ python pancake_sort.py
```

You will be prompted to enter the number of sticks in the stack. The program will shuffle the sticks and display the solution paths and metrics for each search method.

#### Example Output

```bash
Enter the number of sticks: 5

Starting configuration: [3, 5, 1, 4, 2]

Uniform Cost Search (UCS):
Step 1: [3, 5, 1, 4, 2], Cost: 0
...
Total Cost: 12
Total Expanded Nodes: 30
...
```

### Heuristics

1. **Largest Misplaced Stick**: Computes the largest misplaced stick in the stack.
2. **Sum of Distances to the Goal**: Calculates the sum of the absolute distances between current and goal positions of sticks.
3. **Gap Heuristic**: Counts gaps in sequential order in the stack.
4. **Weighted Gap Heuristic**: Weighs gaps by their positions in the stack.

### Algorithms

#### Uniform Cost Search (UCS)
- Explores nodes in increasing order of cost.
- Guarantees optimality but may expand many nodes.

#### A* Search
- Combines path cost and heuristic value.
- Offers a balance between optimality and efficiency.

#### Greedy Search
- Focuses only on heuristic values.
- Faster but not guaranteed to find optimal solutions.

### Metrics Comparison

The script compares search algorithms based on:
- **Total Cost**: The number of flips required to sort the stack.
- **Expanded Nodes**: The total number of nodes expanded during the search.

### Customization

You can add or modify heuristics by editing the functions in the `pancake_sort.py` file. Use the following signature for custom heuristics:

```python
def custom_heuristic(state):
    # Your heuristic logic here
    return heuristic_value
```

### Files

- `pancake_sort.py`: Main implementation of the Pancake Sorting Problem and search algorithms.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

### Author

Created by [Your Name].

### Acknowledgments

Inspired by the Pancake Sorting Problem as a combinatorial optimization challenge.
