# Wordle Solver 🎯

An optimal Wordle solver using information-theoretic strategies to suggest the best next guess. Implements both **average-case** and **minimax** (worst-case) algorithms to help you solve Wordle puzzles efficiently.

## Features ✨

- **Dual Strategy Analysis**: Shows both average-case optimal and minimax (worst-case) optimal suggestions
- **Pattern Grouping Algorithm**: Uses the standard information-theoretic approach to evaluate guesses
- **O(n²) Performance**: Efficiently analyzes all candidate words, even with large word lists
- **Smart Tiebreaking**: Minimax uses average-case as tiebreaker when worst cases are equal
- **Interactive CLI**: Simple terminal interface for step-by-step solving
- **Detailed Statistics**: Shows remaining possibilities, known constraints, and expected outcomes

## Installation

### Prerequisites

- Python 3.6 or higher (uses only standard library, no external deps)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/SebPit/wordl_solver.git
cd wordl_solver
```

2. Create your word list file (`wordl_list.txt`) with space-separated 5-letter words:
```
about above abuse actor acute admit adopt adult after again
...
```

You can use the [official Wordle word list](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b) or any custom word list. A copy of the list is part of the repository.

## Usage 💻

Run the solver:
```bash
python wordle_solver.py
```

### How to Use

1. The solver suggests the best word to guess
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
   Word: RAISE
   Average remaining: 61.72 | Worst case: 170

🛡️  BEST FOR WORST CASE (Minimax):
   Word: RAISE
   Average remaining: 61.72 | Worst case: 170
   (When tied on worst case, picks best average)

✨ Both strategies agree!
------------------------------------------------------------

Enter your guess (or command): RAISE
Enter the result (5 digits, 0/1/2): 01002

------------------------------------------------------------
Possible words remaining: 12
Known positions: {4: 'E'}
Known letters (wrong position): {'A', 'I'}
Excluded letters: {'R', 'S'}

💡 BEST FOR AVERAGE CASE:
   Word: ALIEN
   Average remaining: 2.33 | Worst case: 5

🛡️  BEST FOR WORST CASE (Minimax):
   Word: ALIVE
   Average remaining: 2.50 | Worst case: 4
   (When tied on worst case, picks best average)
------------------------------------------------------------
```

### Commands

- `quit` or `exit` - Exit the program
- `reset` - Start over with a new puzzle
- `show` - Display all remaining possible words

## Algorithm Explanation 🧮

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

## Performance ⚡

- **Complexity**: O(n²) where n is the number of remaining words
- **Typical Analysis Time**: 
  - 2,344 words (full list): ~2-5 seconds
  - 100 words: <0.5 seconds
  - <20 words: Nearly instant

## File Structure 📁

```
wordl_solver/
├── wordle_solver.py    # Main solver script
├── wordl_list.txt      # Your word list (space-separated)
└── README.md           # This file
```

## License 📄

MIT License - feel free to use and modify as needed.

## Tips 💡

1. **First guess**: On a full word list, RAISE, SOARE, or ARISE are typically optimal
2. **Strategy choice**: Use average-case for typical play, minimax if you want consistency
3. **Hard mode**: The solver doesn't enforce hard mode constraints, but you can manually follow them
4. **Custom word lists**: You can use different word lists for practice or different variants

---
