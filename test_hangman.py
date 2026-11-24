"""
Automated Test Suite for Hangman Game
Tests game logic, masking, stages, input validation, and full gameplay simulations.
"""

import unittest
from unittest.mock import patch
import io
import sys

import hangman


class TestHangmanCoreLogic(unittest.TestCase):
    def test_word_selection(self):
        """Test random word selection returns valid uppercase words from list."""
        for _ in range(20):
            word = hangman.get_random_word(hangman.WORDS)
            self.assertIn(word, hangman.WORDS)
            self.assertTrue(word.isupper())
            self.assertTrue(word.isalpha())

    def test_ascii_stages(self):
        """Verify exactly 7 ASCII gallows stages exist (stages 0 to 6)."""
        self.assertEqual(len(hangman.HANGMAN_STAGES), 7)
        for stage in hangman.HANGMAN_STAGES:
            self.assertIn("+---+", stage)
            self.assertIn("=========", stage)

    def test_masked_word_formatting(self):
        """Verify word masking with underscores and spaces."""
        word = "HANGMAN"
        
        # No letters guessed
        self.assertEqual(hangman.get_masked_word(word, set()), "_ _ _ _ _ _ _")
        
        # Partial guesses
        self.assertEqual(hangman.get_masked_word(word, {"A"}), "_ A _ _ _ A _")
        self.assertEqual(hangman.get_masked_word(word, {"A", "N"}), "_ A N _ _ A N")
        self.assertEqual(hangman.get_masked_word(word, {"A", "H", "N"}), "H A N _ _ A N")
        
        # Irrelevant guess
        self.assertEqual(hangman.get_masked_word(word, {"Z"}), "_ _ _ _ _ _ _")
        
        # Fully guessed
        self.assertEqual(hangman.get_masked_word(word, {"H", "A", "N", "G", "M"}), "H A N G M A N")

    def test_display_game_status_output(self):
        """Verify display_game_status prints correct attempt and masked word information."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            hangman.display_game_status(
                secret_word="PYTHON",
                guessed_letters={"P", "Y", "Z"},
                incorrect_letters={"Z"},
                max_attempts=6
            )
        output = captured.getvalue()
        self.assertIn("MISTAKES: 1/6", output)
        self.assertIn("ATTEMPTS REMAINING: 5", output)
        self.assertIn("P Y _ _ _ _", output)
        self.assertIn("Incorrect Guesses: Z", output)
        self.assertIn("All Guessed Letters: P, Y, Z", output)


class TestInputValidation(unittest.TestCase):
    @patch("builtins.input", side_effect=["", "12", "#", "ab", "a"])
    def test_get_valid_guess_rejection_of_invalid_inputs(self, mock_input):
        """Ensure non-single-alphabet characters are rejected until a valid letter is given."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            guess = hangman.get_valid_guess(guessed_letters=set())
        
        self.assertEqual(guess, "A")
        output = captured.getvalue()
        self.assertIn("Please enter exactly ONE letter at a time", output)
        self.assertIn("Invalid character! Please enter an alphabetic letter (A-Z)", output)

    @patch("builtins.input", side_effect=["x", "y"])
    def test_get_valid_guess_duplicate_prevention(self, mock_input):
        """Ensure already guessed letters are caught and prompted again without crash."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            guess = hangman.get_valid_guess(guessed_letters={"X"})
        
        self.assertEqual(guess, "Y")
        output = captured.getvalue()
        self.assertIn("You already guessed 'X'", output)

    @patch("builtins.input", side_effect=["maybe", "yes"])
    def test_ask_play_again_yes(self, mock_input):
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            self.assertTrue(hangman.ask_play_again())

    @patch("builtins.input", side_effect=["no"])
    def test_ask_play_again_no(self, mock_input):
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            self.assertFalse(hangman.ask_play_again())


class TestGameplaySimulations(unittest.TestCase):
    @patch("hangman.get_random_word", return_value="PYTHON")
    @patch("builtins.input", side_effect=["p", "y", "t", "h", "o", "n"])
    def test_simulated_win_round(self, mock_input, mock_word):
        """Simulate a game where user guesses all correct letters."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            hangman.play_game()
        output = captured.getvalue()
        self.assertIn("CONGRATULATIONS! YOU WON!", output)
        self.assertIn("You correctly solved the secret word: PYTHON", output)

    @patch("hangman.get_random_word", return_value="PYTHON")
    # Feed 6 wrong letters: A, B, C, D, E, F
    @patch("builtins.input", side_effect=["a", "b", "c", "d", "e", "f"])
    def test_simulated_loss_round(self, mock_input, mock_word):
        """Simulate a game where player exhausts all 6 incorrect attempts."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            hangman.play_game()
        output = captured.getvalue()
        self.assertIn("GAME OVER! YOU WERE HANGED!", output)
        self.assertIn("The secret word was: PYTHON", output)

    @patch("hangman.get_random_word", return_value="CODE")
    # Mix of correct, wrong, duplicate, and invalid entries
    @patch("builtins.input", side_effect=["c", "c", "!", "o", "x", "x", "d", "e"])
    def test_mixed_gameplay_with_duplicates_and_invalids(self, mock_input, mock_word):
        """Ensure duplicate guesses and bad inputs do not cause loss of attempts or crash."""
        captured = io.StringIO()
        with patch("sys.stdout", captured):
            hangman.play_game()
        output = captured.getvalue()
        self.assertIn("CONGRATULATIONS! YOU WON!", output)
        self.assertIn("You already guessed 'C'", output)
        self.assertIn("You already guessed 'X'", output)
        self.assertIn("Invalid character", output)


if __name__ == "__main__":
    unittest.main()
