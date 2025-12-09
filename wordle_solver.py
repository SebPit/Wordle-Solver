#!/usr/bin/env python3
"""
Wordle Solver - Interactive terminal script with Minimax strategy
Usage: python wordle_solver.py
"""

import string
from collections import Counter, defaultdict
from typing import List, Set, Dict, Tuple


def load_word_list(filename: str = "wordle_list.txt") -> List[str]:
    """Load words from a space-separated text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split by whitespace (spaces, tabs, newlines)
            words = content.split()
            print(f"✓ Loaded {len(words)} words from {filename}")
            return words
    except FileNotFoundError:
        raise FileNotFoundError


class WordleSolver:
    def __init__(self, word_list: List[str]):
        self.all_words = [w.upper() for w in word_list]
        self.possible_words = self.all_words.copy()
        self.known_positions: Dict[int, str] = {}  # position -> letter (green)
        self.known_letters: Set[str] = set()  # letters in word but position unknown (yellow)
        self.wrong_positions: Dict[str, Set[int]] = {}  # letter -> set of wrong positions
        self.excluded_letters: Set[str] = set()  # letters not in word (gray)
        
    def reset(self):
        """Reset the solver state"""
        self.possible_words = self.all_words.copy()
        self.known_positions = {}
        self.known_letters = set()
        self.wrong_positions = {}
        self.excluded_letters = set()
    
    @staticmethod
    def get_feedback_pattern(guess: str, answer: str) -> str:
        """
        Calculate the feedback pattern for a guess against an answer.
        Returns a string of 5 digits (0=gray, 1=yellow, 2=green)
        """
        guess = guess.upper()
        answer = answer.upper()
        result = ['0'] * 5
        answer_letters = list(answer)
        
        # First pass: mark greens (correct position)
        for i in range(5):
            if guess[i] == answer[i]:
                result[i] = '2'
                answer_letters[i] = None  # Mark as used
        
        # Second pass: mark yellows (wrong position)
        for i in range(5):
            if result[i] == '0' and guess[i] in answer_letters:
                result[i] = '1'
                # Remove first occurrence from answer_letters
                answer_letters[answer_letters.index(guess[i])] = None
        
        return ''.join(result)
    
    def parse_feedback(self, word: str, feedback: str) -> bool:
        """
        Parse the feedback string and update constraints
        word: the guessed word (5 letters)
        feedback: string of 5 digits (0=wrong, 1=wrong position, 2=correct)
        """
        if len(word) != 5 or len(feedback) != 5:
            return False
        
        word = word.upper()
        
        # First pass: identify all letters that are in the word (yellows and greens)
        letters_in_word = set()
        for i, (letter, result) in enumerate(zip(word, feedback)):
            if result in ('1', '2'):
                letters_in_word.add(letter)
        
        # Second pass: process each position
        for i, (letter, result) in enumerate(zip(word, feedback)):
            if result == '2':  # Correct position (green)
                self.known_positions[i] = letter
                if letter not in self.known_letters:
                    self.known_letters.add(letter)
            elif result == '1':  # Wrong position (yellow)
                self.known_letters.add(letter)
                if letter not in self.wrong_positions:
                    self.wrong_positions[letter] = set()
                self.wrong_positions[letter].add(i)
            elif result == '0':  # Not in word (gray)
                # Only exclude if this letter isn't marked as yellow/green elsewhere
                if letter not in letters_in_word:
                    self.excluded_letters.add(letter)
                else:
                    # Letter exists but not in this position
                    if letter not in self.wrong_positions:
                        self.wrong_positions[letter] = set()
                    self.wrong_positions[letter].add(i)
        
        return True
    
    def is_valid_word(self, word: str) -> bool:
        """Check if a word satisfies all current constraints"""
        word = word.upper()
        
        # Check excluded letters
        for letter in self.excluded_letters:
            if letter in word:
                return False
        
        # Check known positions (green)
        for pos, letter in self.known_positions.items():
            if word[pos] != letter:
                return False
        
        # Check known letters are in word (yellow)
        for letter in self.known_letters:
            if letter not in word:
                return False
        
        # Check wrong positions (yellow constraints)
        for letter, wrong_positions in self.wrong_positions.items():
            for pos in wrong_positions:
                if word[pos] == letter:
                    return False
        
        return True
    
    def filter_words(self):
        """Filter possible words based on current constraints"""
        self.possible_words = [w for w in self.possible_words if self.is_valid_word(w)]
    
    def calculate_score(self, word: str, possible_solutions: List[str]) -> Tuple[float, int]:
        """
        Calculate both the average and worst-case number of remaining words after this guess.
        
        Algorithm (Pattern Grouping):
        1. For each possible answer, simulate what feedback pattern we'd get
        2. Group answers by their feedback pattern
        3. Each group represents answers we CAN'T distinguish with this guess
        4. Group size = how many words remain if we get that pattern
        
        Example:
          Guess "ALERT" with possible answers [WRITE, WHITE, QUITE]
          - WRITE → pattern "00210" 
          - WHITE → pattern "00210" (same as WRITE!)
          - QUITE → pattern "00012"
          
          Groups: {"00210": 2 words, "00012": 1 word}
          
          Average: (2² + 1²) / 3 = 5/3 = 1.67 words expected
          Worst case: max(2, 1) = 2 words in worst scenario
        
        This is the standard information-theoretic approach for Wordle solvers.
        
        Returns: (average_remaining, worst_case_remaining)
        """
        # Group solutions by their feedback pattern
        pattern_groups = defaultdict(int)
        
        for sol in possible_solutions:
            pattern = self.get_feedback_pattern(word, sol)
            pattern_groups[pattern] += 1
        
        # Calculate statistics from group sizes
        group_sizes = list(pattern_groups.values())
        
        if not group_sizes:
            return 0, 0
        
        # Average: each group of size n contributes n²/total to expected value
        # (probability n/total × remaining n = n²/total)
        average = sum(size * size for size in group_sizes) / len(possible_solutions)
        
        # Worst case: largest group (unluckiest pattern we could get)
        worst_case = max(group_sizes)
        
        return average, worst_case
    
    def suggest_next_word(self) -> Dict[str, Tuple[str, float, int]]:
        """
        Suggest the best next words using both strategies.
        Returns: {
            'average': (word, avg_remaining, worst_case),
            'minimax': (word, avg_remaining, worst_case)
        }
        """
        if not self.possible_words:
            return None
        
        if len(self.possible_words) == 1:
            word = self.possible_words[0]
            return {
                'average': (word, 0, 0),
                'minimax': (word, 0, 0)
            }
        
        # Calculate both scores for all candidates
        candidates = self.possible_words
        
        best_avg_word = None
        best_avg_score = float('inf')
        best_avg_worst = None
        
        best_minimax_word = None
        best_minimax_score = float('inf')
        best_minimax_avg = None
        
        print(f"🔍 Analyzing {len(candidates)} candidates...", end='', flush=True)
        
        for i, word in enumerate(candidates):
            if i % 20 == 0 and i > 0:
                print(f"\r🔍 Analyzing {len(candidates)} candidates... ({i}/{len(candidates)})", end='', flush=True)
            
            avg_score, worst_score = self.calculate_score(word, self.possible_words)
            
            # Track best for average-case
            if avg_score < best_avg_score:
                best_avg_score = avg_score
                best_avg_word = word
                best_avg_worst = worst_score
            
            # Track best for worst-case (minimax) with average as tiebreaker
            if (worst_score < best_minimax_score or 
                (worst_score == best_minimax_score and avg_score < best_minimax_avg)):
                best_minimax_score = worst_score
                best_minimax_word = word
                best_minimax_avg = avg_score
        
        print(f"\r🔍 Analysis complete!                                    ")
        
        return {
            'average': (best_avg_word, best_avg_score, best_avg_worst),
            'minimax': (best_minimax_word, best_minimax_avg, best_minimax_score)
        }
    
    def get_stats(self) -> str:
        """Get current statistics"""
        lines = [
            f"Possible words remaining: {len(self.possible_words)}",
            f"Known positions: {dict(self.known_positions)}",
            f"Known letters (wrong position): {self.known_letters - set(self.known_positions.values())}",
            f"Excluded letters: {self.excluded_letters}"
        ]
        return "\n".join(lines)


def main():
    print("=" * 60)
    print("WORDLE SOLVER - DUAL STRATEGY")
    print("=" * 60)
    print("\nHow to use:")
    print("1. Enter your guess (5 letters)")
    print("2. Enter the result (5 digits):")
    print("   0 = Letter not in word (gray)")
    print("   1 = Letter in word, wrong position (yellow)")
    print("   2 = Letter in correct position (green)")
    print("\nExample:")
    print("   STAGE")
    print("   01002")
    print("\nCommands:")
    print("   'quit' or 'exit' - Exit the program")
    print("   'reset' - Start over with a new puzzle")
    print("   'show' - Show all remaining possible words")
    print("=" * 60)
    
    # Load word list
    try:
        word_list = load_word_list()
    except FileNotFoundError:
        print("\n❌ Error: wordle_list.txt not found!")
        print("Please create a file named 'wordle_list.txt' with space-separated words.")
        return
    
    solver = WordleSolver(word_list)
    
    while True:
        print(f"\n{'-' * 60}")
        print(solver.get_stats())
        
        # Suggest next word
        suggestions = solver.suggest_next_word()
        if not suggestions:
            print("\n❌ No possible words found!")
            print("\nThis usually means:")
            print("  1. You entered a word that's not in the word list")
            print("  2. There was an error in the feedback pattern")
            print("  3. The answer isn't in your word list")
            print("\nOptions:")
            print("  - Type 'reset' to start over")
            print("  - Type 'quit' to exit")
            
            choice = input("\nWhat would you like to do? ").strip().lower()
            if choice in ['quit', 'exit']:
                print("Thanks for playing!")
                break
            elif choice == 'reset':
                solver.reset()
                print("\n♻️  Solver reset! Starting fresh...")
                continue
            else:
                continue
        
        avg_word, avg_score, avg_worst = suggestions['average']
        mini_word, mini_avg, mini_score = suggestions['minimax']
        
        print("\n💡 BEST FOR AVERAGE CASE:")
        print(f"   Word: {avg_word}")
        print(f"   Average remaining: {avg_score:.2f} | Worst case: {avg_worst}")
        
        print("\n🛡️  BEST FOR WORST CASE (Minimax):")
        print(f"   Word: {mini_word}")
        print(f"   Average remaining: {mini_avg:.2f} | Worst case: {mini_score}")
        print("   (When tied on worst case, picks best average)")
        
        if avg_word == mini_word:
            print("\n✨ Both strategies agree!")
        
        print(f"{'-' * 60}")
        
        # Get word input
        word_input = input("\nEnter your guess (or command): ").strip().upper()
        
        if word_input in ['QUIT', 'EXIT']:
            print("Thanks for playing!")
            break
        
        if word_input == 'RESET':
            solver.reset()
            print("\n♻️  Solver reset! Starting fresh...")
            continue
        
        if word_input == 'SHOW':
            if len(solver.possible_words) <= 50:
                print("\nAll possible words:")
                for i, word in enumerate(sorted(solver.possible_words), 1):
                    print(f"  {i:2d}. {word}")
            else:
                print(f"\nToo many words to display ({len(solver.possible_words)})")
                print("First 20:", ", ".join(sorted(solver.possible_words)[:20]))
            continue
        
        if len(word_input) != 5:
            print("❌ Error: Word must be exactly 5 letters!")
            continue
        
        # Get feedback input
        feedback_input = input("Enter the result (5 digits, 0/1/2): ").strip()
        
        if len(feedback_input) != 5 or not all(c in '012' for c in feedback_input):
            print("❌ Error: Result must be exactly 5 digits (0, 1, or 2)!")
            continue
        
        # Check if solved
        if feedback_input == '22222':
            print("\n🎉 Congratulations! You solved it!")
            play_again = input("Play again? (yes/no): ").strip().lower()
            if play_again in ['yes', 'y']:
                solver.reset()
                print("\n♻️  Starting new puzzle...")
            else:
                print("Thanks for playing!")
                break
            continue
        
        # Process feedback
        if not solver.parse_feedback(word_input, feedback_input):
            print("❌ Error parsing feedback!")
            continue
        
        # Filter words based on new constraints
        solver.filter_words()


if __name__ == "__main__":
    main()
