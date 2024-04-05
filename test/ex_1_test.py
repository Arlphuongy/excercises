""" Exercise 1 Test """

import io
import sys
import unittest
import os
from ex_1 import BeginnerExercises

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestBeginnerExercises(unittest.TestCase):
    """Test Beginner Exercises"""

    def setUp(self):
        """Set up the test fixture before each test method."""
        self.exercises = BeginnerExercises()

    def test_is_palindrome(self):
        """Test the is_palindrome method."""
        self.assertEqual(self.exercises.is_palindrome("racecar"), "is a palindrome")
        self.assertEqual(self.exercises.is_palindrome("hello"), "is not a palindrome")
        self.assertEqual(self.exercises.is_palindrome("Madam"), "is a palindrome")
        self.assertEqual(
            self.exercises.is_palindrome("A man, a plan, a canal, Panama!"),
            "is a palindrome",
        )
        self.assertEqual(
            self.exercises.is_palindrome("No 'x' in Nixon"), "is a palindrome"
        )
        self.assertEqual(self.exercises.is_palindrome(""), "is a palindrome")

    def test_fizzbuzz(self):
        """Test the fizzbuzz method."""
        # Capture the output of fizzbuzz to a string

        code_output = io.StringIO()  # Create StringIO object
        sys.stdout = code_output  # Redirect stdout.
        self.exercises.fizzbuzz()  # Call function.
        sys.stdout = sys.__stdout__  # Reset redirect.

        # Check the first few lines of the output
        lines = code_output.getvalue().split("\n")
        self.assertEqual(lines[0], "1")
        self.assertEqual(lines[2], "fizz")
        self.assertEqual(lines[4], "buzz")
        self.assertIn("fizzbuzz", lines)  # Ensure fizzbuzz is in the output

    def test_find_max(self):
        """Test the find_max method."""
        self.assertEqual(self.exercises.find_max([1, 3, 2]), 3)
        self.assertEqual(self.exercises.find_max([-10, -20, -30]), -10)
        self.assertEqual(self.exercises.find_max([10]), 10)
        self.assertEqual(self.exercises.linear_search([1, 4, 5, 5, 7], 5), 2)
        self.assertEqual(self.exercises.find_max([1, 3, 3, 2]), 3)
        self.assertEqual(self.exercises.find_max([-10, -10, -20, -30]), -10)
        self.assertEqual(self.exercises.find_max([7, 7, 7, 7]), 7)

    def test_linear_search(self):
        """Test the linear_search method."""
        self.assertEqual(self.exercises.linear_search([1, 4, 5, 2, 7], 5), 2)
        self.assertEqual(self.exercises.linear_search([1, 4, 5, 2, 7], 3), -1)
        self.assertEqual(self.exercises.linear_search([], 1), -1)
        self.assertEqual(self.exercises.linear_search([-1, -4, -5, -2, -7], -5), 2)
        self.assertEqual(self.exercises.linear_search([-1, -4, -5, -2, -7], 1), -1)


if __name__ == "__main__":
    unittest.main()
