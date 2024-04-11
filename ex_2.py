""" Exercise 2 """


class IntermediateExercises:
    """Intermediate Exercises"""

    def linear_search(self, arr, target):
        """Implement linear search algorithm to find given element in list and return its index, if not in list return -1"""
        for index, item in enumerate(arr):
            if item == target:
                return index
        return -1

    def binary_search(self, arr, target):
        """Implement binary search algorithm to find position of the selected element in a sorted list"""
        begin = 0
        end = len(arr) - 1

        while begin <= end:
            mid = (begin + end) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                begin = mid + 1
            else:
                end = mid - 1

        return -1

    def bubble_sort(self, arr):
        """Implement bubble sort to sort a list of numbers in ascending order"""
        for i in range(len(arr)):
            switch = False
            for j in range(0, len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    switch = True
            if not switch:
                break
        return arr

    def factorial(self, n):
        """Calculate the factorial of a non-negative integer using an iterative method"""
        product = 1
        for i in range(1, n + 1):
            product *= i
        return product

    def is_prime(self, n):
        """Check if a given number is prime"""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def fibonacci(self, n):
        """Generate the first 'n' Fibonacci numbers using an iterative approach"""
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        else:
            fib_list = [0, 1]
            for _ in range(2, n):
                fib_list.append(fib_list[-1] + fib_list[-2])
            return fib_list


if __name__ == "__main__":
    exercises = IntermediateExercises()

    # Test linear search
    print(exercises.linear_search([1, 4, 5, 2, 7], 5))
    print(exercises.linear_search([1, 4, 5, 2, 7], 3))

    # Test binary search
    print(exercises.binary_search([1, 2, 3, 4, 5], 3))
    print(exercises.binary_search([1, 2, 3, 4, 5], 6))

    # Test bubble sort
    print(exercises.bubble_sort([5, 3, 2, 4, 1]))

    # Test factorial
    print(exercises.factorial(5))

    # Test prime
    print(exercises.is_prime(7))

    # Test Fibonacci
    print(exercises.fibonacci(10))
