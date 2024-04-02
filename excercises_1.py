""" Exercise 1 Beginner"""


def question1():
    """write a function that checks whether a string is a palindrome"""

    def is_palindrome(s):
        new_s = s[::-1]
        if new_s == s:
            return "is a palindrome"
        else:
            return "is not a palindrome"

    print(is_palindrome("hello"))
    print(is_palindrome("ollo"))


def question2():
    """write program where for multiples of three, it'll print out fizz. for multiples of 5,
    it'll print out buzz. for multiples of both 3 and 5 it'll print out fizzbuzz
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


def question3():
    """write a function that takes a list of numbers and returns the largest number without using max()"""

    def find_max(numbers):
        numbers.sort()
        return numbers[-1]

    print(find_max([1, 2, 3]))
    print(find_max([-10, -2, -3]))


def question4():
    """implement linear search algorithm to find given element in list and return its index, if not in list return -1"""

    def linear_search(list, target):
        for i in enumerate(list):
            if list[i] == target:
                return i
        return -1

    print(linear_search([1, 4, 5, 2, 7], 5))
    print(linear_search([1, 4, 5, 2, 7], 3))


if __name__ == "__main__":
    question1()
    question2()
    question3()
    question4()
