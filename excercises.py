#write a function that checks whether a string is a palindrome
def is_palindrome(s):
    new_s = s [::-1]
    if new_s == s:
        return "is a palindrome"
    else:
        return "is not a palindrome"

print(is_palindrome("hello"))
print(is_palindrome("ollo"))

#write program where for multiples of three, it'll print out fizz. for multiples of 5, it'll print out buzz. for multiples of both
#3 and 5 it'll print out fizzbuzz
for i in range (1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("fizzbuzz")
    elif i % 3 == 0:
        print("fizz")
    elif i % 5 == 0:
        print("buzz")
    else:
        print(i)

#write a function that takes a list of numbers and returns the largest number without using max()
def find_max(numbers):
    numbers.sort()
    return numbers[-1]

print(find_max([1,2,3]))
print(find_max([-10,-2,-3]))

# implement linear search algorithm to find given element in list and return its index, if not in list return -1
def linear_search(list, target):
    for i in range(0, len(list)):
        if list[i] == target:
            return i
    return -1
    
print(linear_search([1,4,5,2,7], 5))
print(linear_search([1,4,5,2,7], 3))

#implement binary search algorithm to find position of the selected element in a sorted list
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
    return - 1        

print(binary_search([1,2,3,4,5], 3))
print(binary_search([1,2,3,4,5], 6))

#implement bubble sort to sort a list of numbers in ascending order
def bubble_sort(list):
    for i in range (len(list)):
        switch = False
        for j in range (0, len(list) - i - 1):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]
                switch = True
        if switch == False:
            break
    return list

print(bubble_sort([5,3,2,4,1]))