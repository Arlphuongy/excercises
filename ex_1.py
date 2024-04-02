""" Exercise 1 """


class BeginnerExercises:
    """Beginner Exercises"""

    def is_palindrome(self, s):
        """Check whether a string is a palindrome, ignoring spaces, punctuation, and case."""
        # Filter out non-alphanumeric characters and convert to lowercase
        filtered_s = "".join(char.lower() for char in s if char.isalnum())

        # Reverse the filtered string
        new_s = filtered_s[::-1]

        # Compare the filtered string with its reverse
        return "is a palindrome" if new_s == filtered_s else "is not a palindrome"

    def fizzbuzz(self):
        """Print 'fizz' for multiples of 3, 'buzz' for multiples of 5,
        and 'fizzbuzz' for multiples of both.
        """
        for i in range(1, 101):
            if i % 3 == 0 and i % 5 == 0:
                print("fizzbuzz")
            elif i % 3 == 0:
                print("fizz")
            elif i % 5 == 0:
                print("buzz")
            else:
                print(i)

    def find_max(self, numbers):
        """Return the largest number in a list without using max()."""
        largest = numbers[0]
        for number in numbers[1:]:
            if number > largest:
                largest = number
        return largest

    def linear_search(self, list, target):
        """Perform a linear search and return the index of 'target' in 'list', or -1 if not found."""
        for index, value in enumerate(list):
            if value == target:
                return index
        return -1


if __name__ == "__main__":
    exercises = BeginnerExercises()

    # Test palindrome
    print(exercises.is_palindrome("Madam"))
    print(exercises.is_palindrome("A man, a plan, a canal, Panama!"))

    # Run fizzbuzz
    # exercises.fizzbuzz()

    # # Test find_max
    # print(exercises.find_max([1, 2, 3]))
    # print(exercises.find_max([-10, -2, -3]))

    # # Test linear search
    # print(exercises.linear_search([1, 4, 5, 2, 7], 5))
    # print(exercises.linear_search([1, 4, 5, 2, 7], 3))
