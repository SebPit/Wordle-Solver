# Wordle Solver

An optimal Wordle solver using information-theoretic strategies to suggest the best next guess. Implements both **average-case** and **minimax** (worst-case) algorithms to help you solve Wordle puzzles efficiently.

## Features

- **Dual Strategy Analysis**: Shows both average-case optimal and minimax (worst-case) optimal suggestions
- **Top 3 Suggestions**: Displays the top 3 word choices for each strategy, giving you options
- **Custom Word Lists**: Pass your own word list as a command-line argument
- **Pattern Grouping Algorithm**: Uses the standard information-theoretic approach to evaluate guesses
- **O(n²) Performance**: Efficiently analyzes all candidate words, even with large word lists
- **Smart Tiebreaking**: Minimax uses average-case as tiebreaker when worst cases are equal
- **Interactive CLI**: Simple terminal interface for step-by-step solving
- **Detailed Statistics**: Shows remaining possibilities, known constraints, and expected outcomes

## Installation

### Prerequisites

- Python 3.6 or higher (uses only standard library, no external dependencies)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wordle_solver.git
cd wordle_solver
```

2. Create your word list file (`wordle_list.txt`) with space-separated 5-letter words:
```
about above abuse actor acute admit adopt adult after again
...
```

You can use the [official Wordle word list](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b) or any custom word list.

## Usage

Run the solver:
```bash
# Use default word list (wordle_list.txt)
python wordle_solver.py

# Use a custom word list
python wordle_solver.py my_custom_words.txt

# Show help
python wordle_solver.py --help
```

### How to Use

1. The solver suggests the **top 3 words** for both average-case and minimax strategies
2. Enter your guess in Wordle
3. Enter the result pattern using:
   - `0` = Letter not in word (gray)
   - `1` = Letter in word, wrong position (yellow)
   - `2` = Letter in correct position (green)

### Example Session

```
============================================================
WORDLE SOLVER - DUAL STRATEGY
============================================================

------------------------------------------------------------
Possible words remaining: 2344
Known positions: {}
Known letters (wrong position): set()
Excluded letters: set()

💡 BEST FOR AVERAGE CASE:
   1. RAISE    → Avg: 61.72 | Worst: 170
   2. ARISE    → Avg: 64.61 | Worst: 170
   3. SOARE    → Avg: 65.30 | Worst: 168

🛡️  BEST FOR WORST CASE (Minimax):
   1. SOARE    → Avg: 65.30 | Worst: 168
   2. RAISE    → Avg: 61.72 | Worst: 170
   3. ARISE    → Avg: 64.61 | Worst: 170
------------------------------------------------------------

Enter your guess (or command): RAISE
Enter the result (5 digits, 0/1/2): 01002

------------------------------------------------------------
Possible words remaining: 12
Known positions: {4: 'E'}
Known letters (wrong position): {'A', 'I'}
Excluded letters: {'R', 'S'}

💡 BEST FOR AVERAGE CASE:
   1. ALIEN    → Avg:  2.33 | Worst:   5
   2. ATONE    → Avg:  2.50 | Worst:   4
   3. AXITE    → Avg:  2.67 | Worst:   5

🛡️  BEST FOR WORST CASE (Minimax):
   1. ATONE    → Avg:  2.50 | Worst:   4
   2. ALIEN    → Avg:  2.33 | Worst:   5
   3. ALIKE    → Avg:  2.83 | Worst:   5
------------------------------------------------------------
```

### Commands

- `quit` or `exit` - Exit the program
- `reset` - Start over with a new puzzle
- `show` - Display all remaining possible words

## Algorithm Explanation

### Pattern Grouping

The solver uses the **pattern grouping** algorithm, which is the standard information-theoretic approach:

1. **For each candidate word**, simulate what would happen if each possible answer were correct
2. **Group answers by feedback pattern** - answers producing the same pattern are indistinguishable
3. **Calculate metrics**:
   - **Average-case**: Expected number of remaining words = Σ(group_size²) / total_words
   - **Worst-case**: Size of the largest group (unluckiest scenario)

### Example

Guess `ALERT` with possible answers `[WRITE, WHITE, QUITE, STARE, LATER]`:

```
WRITE → pattern "00210" ┐
WHITE → pattern "00210" ├─ Group A: 2 words (indistinguishable!)
                        ┘
QUITE → pattern "00012" ─  Group B: 1 word
STARE → pattern "11222" ─  Group C: 1 word  
LATER → pattern "22222" ─  Group D: 1 word (solved!)

Average = (2² + 1² + 1² + 1²) / 5 = 1.4 words
Worst case = max(2, 1, 1, 1) = 2 words
```

### Two Strategies

**Average-Case (Recommended)**
- Minimizes expected remaining words
- Best typical performance
- Used by most competitive Wordle solvers

**Minimax (Conservative)**
- Minimizes worst-case remaining words
- Guarantees you won't get very unlucky
- Uses average as tiebreaker

## Performance

- **Complexity**: O(n²) where n is the number of remaining words
- **Typical Analysis Time**: 
  - 2,344 words (full list): ~2-5 seconds
  - 100 words: <0.5 seconds
  - <20 words: Nearly instant

## File Structure

```
wordle_solver/
├── wordle_solver.py    # Main solver script
├── wordle_list.txt      # Your word list (space-separated)
├── *_list.txt      # other word lists
└── README.md           # This file
```

## License

MIT License - feel free to use and modify as needed.
