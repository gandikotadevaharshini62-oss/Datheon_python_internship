"""
Terminal-Based Hangman Game in Python
Author: Antigravity Assistant

A classic, interactive word-guessing game designed for the terminal.
Features:
- Random word selection from a categorized, curated word list
- 7-stage ASCII gallows visualization
- Robust input validation (single alphabetic characters only)
- Set-based tracking of guessed letters and incorrect attempts
- Attempt management (6 maximum incorrect attempts; duplicates don't penalize)
- Clear status display (masked word, remaining attempts, wrong guesses)
- Victory and game-over screens revealing the secret word
- Replay functionality with fresh random words
"""

import random
import sys

# ---------------------------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------------------------

MAX_INCORRECT_ATTEMPTS = 6

# Predefined list of English words of diverse categories and lengths
WORDS = [
    # Programming & Tech
    "PYTHON", "VARIABLE", "FUNCTION", "ALGORITHM", "KEYBOARD",
    "TERMINAL", "SOFTWARE", "DATABASE", "NETWORK", "COMPILER",
    # Animals & Nature
    "ELEPHANT", "DOLPHIN", "KANGAROO", "PENGUIN", "BUTTERFLY",
    "BLOSSOM", "SUNSHINE", "VOLCANO", "GLACIER", "HORIZON",
    # General & Everyday
    "ADVENTURE", "MYSTERY", "PYRAMID", "TRIANGLE", "JOURNEY",
    "DIAMOND", "WHISPER", "TREASURE", "CHALLENGE", "CHAMPION",
    # Science & Space
    "GALAXY", "GRAVITY", "ASTRONAUT", "ECLIPSE", "TELESCOPE"
]

# 7 stages of ASCII gallows art (indices 0 to 6)
# Stage 0: 0 mistakes (empty gallows)
# Stage 6: 6 mistakes (complete hangman figure)
HANGMAN_STAGES = [
    # Stage 0: 0 incorrect attempts
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    # Stage 1: 1 incorrect attempt (Head)
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    # Stage 2: 2 incorrect attempts (Head + Torso)
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    # Stage 3: 3 incorrect attempts (Head + Torso + Left Arm)
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    # Stage 4: 4 incorrect attempts (Head + Torso + Both Arms)
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    # Stage 5: 5 incorrect attempts (Head + Torso + Arms + Left Leg)
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    # Stage 6: 6 incorrect attempts (Full Hangman - Game Over)
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """
]


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def get_random_word(word_list: list) -> str:
    """Select and return a random word from the provided word list in uppercase."""
    return random.choice(word_list).upper()


def get_masked_word(secret_word: str, guessed_letters: set) -> str:
    """
    Format the secret word for display:
    Show guessed letters and replace unguessed letters with underscores,
    separated by spaces for terminal readability (e.g. '_ A _ H _ A N').
    """
    return " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])


def display_game_status(
    secret_word: str,
    guessed_letters: set,
    incorrect_letters: set,
    max_attempts: int = MAX_INCORRECT_ATTEMPTS
) -> None:
    """
    Print the current game state including:
    - ASCII gallows art for the current mistake count
    - Masked secret word
    - Remaining attempts
    - Incorrectly guessed letters
    - All guessed letters
    """
    num_mistakes = len(incorrect_letters)
    remaining_attempts = max_attempts - num_mistakes

    print("\n" + "=" * 55)
    print(f" MISTAKES: {num_mistakes}/{max_attempts} | ATTEMPTS REMAINING: {remaining_attempts}")
    print("=" * 55)
    
    # Display the corresponding ASCII gallows stage
    print(HANGMAN_STAGES[num_mistakes])
    
    # Display masked word
    masked = get_masked_word(secret_word, guessed_letters)
    print(f" Word:   {masked}   ({len(secret_word)} letters)")
    print("-" * 55)
    
    # Display guess history
    wrong_str = ", ".join(sorted(incorrect_letters)) if incorrect_letters else "None"
    all_str = ", ".join(sorted(guessed_letters)) if guessed_letters else "None"
    
    print(f" Incorrect Guesses: {wrong_str}")
    print(f" All Guessed Letters: {all_str}")
    print("=" * 55)


def get_valid_guess(guessed_letters: set) -> str:
    """
    Prompt the player to enter a single letter.
    Validates input:
    - Must be a single character
    - Must be alphabetic (A-Z)
    - Must not have been previously guessed
    Returns the valid, uppercase single letter.
    """
    while True:
        try:
            raw_input = input("\nEnter your guess (single letter A-Z): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGame aborted by user. Exiting...")
            sys.exit(0)

        # Check for empty input or multi-character input
        if len(raw_input) != 1:
            print(">> [Error] Please enter exactly ONE letter at a time.")
            continue

        # Check if the character is an alphabet letter
        if not raw_input.isalpha():
            print(">> [Error] Invalid character! Please enter an alphabetic letter (A-Z).")
            continue

        guess = raw_input.upper()

        # Check for duplicate guess
        if guess in guessed_letters:
            print(f">> [Note] You already guessed '{guess}'. Please choose a different letter.")
            continue

        return guess


def play_game() -> None:
    """
    Execute a single full round of Hangman:
    - Selects secret word
    - Runs the guess loop
    - Updates game state
    - Declares win or loss and reveals word
    """
    secret_word = get_random_word(WORDS)
    secret_letters = set(secret_word)
    
    # Sets to track player guesses
    guessed_letters = set()      # All guessed letters (both correct and incorrect)
    incorrect_letters = set()    # Only incorrect guesses

    print("\nWelcome to Hangman! Can you guess the secret word before the gallows is complete?")

    # Main guessing loop
    while len(incorrect_letters) < MAX_INCORRECT_ATTEMPTS:
        # Display current stage and status
        display_game_status(secret_word, guessed_letters, incorrect_letters)

        # Check if the player has won
        if secret_letters.issubset(guessed_letters):
            print("\n" + "*" * 55)
            print(" 🌟 CONGRATULATIONS! YOU WON! 🌟")
            print(f" You correctly solved the secret word: {secret_word}")
            print("*" * 55)
            return

        # Prompt for a validated guess
        guess = get_valid_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_letters:
            print(f"\n>> Nice! '{guess}' is in the word!")
        else:
            incorrect_letters.add(guess)
            attempts_left = MAX_INCORRECT_ATTEMPTS - len(incorrect_letters)
            print(f"\n>> Sorry, '{guess}' is NOT in the word. ({attempts_left} attempts left)")

        # Check win condition immediately after guess
        if secret_letters.issubset(guessed_letters):
            display_game_status(secret_word, guessed_letters, incorrect_letters)
            print("\n" + "*" * 55)
            print(" 🌟 CONGRATULATIONS! YOU WON! 🌟")
            print(f" You correctly solved the secret word: {secret_word}")
            print("*" * 55)
            return

    # If loop ends, maximum incorrect attempts reached
    display_game_status(secret_word, guessed_letters, incorrect_letters)
    print("\n" + "!" * 55)
    print(" 💀 GAME OVER! YOU WERE HANGED! 💀")
    print(f" The secret word was: {secret_word}")
    print(" Better luck next time!")
    print("!" * 55)


def ask_play_again() -> bool:
    """
    Ask the user if they want to play another game.
    Accepts 'y', 'yes', 'n', 'no' (case-insensitive).
    """
    while True:
        try:
            choice = input("\nWould you like to play again? (y/n): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            return False

        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print(">> [Error] Please enter 'y' to play again or 'n' to quit.")


def main() -> None:
    """Main program entry point with welcome banner and replay loop."""
    print(r"""
=============================================================
 _   _                                           
| | | | __ _ _ __   __ _ _ __ ___   __ _ _ __   
| |_| |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \  
|  _  | (_| | | | | (_| | | | | | | (_| | | | | 
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_| 
                   |___/                        
            TERMINAL HANGMAN IN PYTHON
=============================================================
Rules:
- A secret word is randomly selected.
- Guess one letter at a time (A-Z).
- You are allowed 6 incorrect attempts.
- Duplicate guesses will NOT cost you an attempt.
- Guess all letters before the figure is hanged to win!
=============================================================
""")
    
    while True:
        play_game()
        if not ask_play_again():
            print("\nThank you for playing Hangman! Goodbye!\n")
            break


if __name__ == "__main__":
    main()
