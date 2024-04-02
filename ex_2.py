""" Exercise 2 Intermediate"""


def question5():
    """implement binary search algorithm to find position of the selected element in a sorted list"""

    def binary_search(sorted_list, target):
        begin = 0
        end = len(sorted_list) - 1

        while begin <= end:
            mid = (begin + end) // 2
            if sorted_list[mid] == target:
                return mid
            elif sorted_list[mid] < target:
                begin = mid + 1
            else:
                end = mid - 1
        return -1

    print(binary_search([1, 2, 3, 4, 5], 3))
    print(binary_search([1, 2, 3, 4, 5], 6))


def question6():
    # implement bubble sort to sort a list of numbers in ascending order
    def bubble_sort(list):
        for i in enumerate(len(list)):
            switch = False
            for j in enumerate(0, len(list) - i - 1):
                if list[j] > list[j + 1]:
                    list[j], list[j + 1] = list[j + 1], list[j]
                    switch = True
            if not switch:
                break
        return list

    print(bubble_sort([5, 3, 2, 4, 1]))


if __name__ == "__main__":
    question5()
    question6()
