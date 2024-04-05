""" Exercise 2 Test """

import unittest
import sys
import os
from ex_2 import IntermediateExercises

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestIntermediateExercises(unittest.TestCase):
    """Test Intermediate Exercises"""

    def setUp(self):
        """Set up the test fixture before each test method."""
        self.exercises = IntermediateExercises()

    def test_linear_search(self):
        """Test the linear_search method."""
        self.assertEqual(self.exercises.linear_search([1, 4, 5, 2, 7], 5), 2)
        self.assertEqual(self.exercises.linear_search([1, 4, 5, 2, 7], 3), -1)
        self.assertEqual(self.exercises.linear_search([], 1), -1)
        self.assertEqual(self.exercises.linear_search([-1, -4, -5, -2, -7], -5), 2)
        self.assertEqual(self.exercises.linear_search([-1, -4, -5, -2, -7], 1), -1)

    def test_binary_search(self):
        """Test the binary_search method."""
        self.assertEqual(self.exercises.binary_search([1, 2, 3, 4, 5], 3), 2)
        self.assertEqual(self.exercises.binary_search([1, 2, 3, 4, 5], 6), -1)
        self.assertEqual(self.exercises.binary_search([], 1), -1)
        self.assertEqual(self.exercises.binary_search([-5, -4, -2, -1], -5), 0)
        self.assertEqual(self.exercises.binary_search([-5, -4, -2, -1], 1), -1)

    def test_bubble_sort(self):
        """Test the bubble_sort method."""
        self.assertEqual(self.exercises.bubble_sort([5, 3, 2, 4, 1]), [1, 2, 3, 4, 5])
        self.assertEqual(self.exercises.bubble_sort([]), [])
        self.assertEqual(self.exercises.bubble_sort([1]), [1])
        self.assertEqual(self.exercises.bubble_sort([3, 2, 1]), [1, 2, 3])

    def test_factorial(self):
        """Test the factorial method."""
        self.assertEqual(self.exercises.factorial(5), 120)
        self.assertEqual(self.exercises.factorial(0), 1)
        self.assertEqual(self.exercises.factorial(1), 1)
        self.assertEqual(self.exercises.factorial(10), 3628800)

    def test_is_prime(self):
        """Test the is_prime method."""
        self.assertTrue(self.exercises.is_prime(7))
        self.assertTrue(self.exercises.is_prime(2))
        self.assertFalse(self.exercises.is_prime(4))
        self.assertFalse(self.exercises.is_prime(1))
        self.assertFalse(self.exercises.is_prime(0))
        self.assertFalse(self.exercises.is_prime(-7))

    def test_fibonacci(self):
        """Test the fibonacci method."""
        self.assertEqual(self.exercises.fibonacci(0), [])
        self.assertEqual(self.exercises.fibonacci(1), [0])
        self.assertEqual(self.exercises.fibonacci(2), [0, 1])
        self.assertEqual(
            self.exercises.fibonacci(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        )


if __name__ == "__main__":
    unittest.main()
