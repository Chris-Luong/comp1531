from typing import List, Iterable, Union, Optional

def multiply_by_two(number: int) -> int:
    '''
    Multiplies a given number by two.
    '''
    return number * 2

def print_message(message: str) -> None:
    '''
    Prints a given message.
    '''
    print(message)

def sum_list_of_numbers(numbers: List[int]) -> int:
    '''
    Returns the sum of a list of numbers
    '''
    return sum(numbers)

def sum_iterable_of_numbers(numbers: Iterable[int]) -> int:
    '''
    Calculates the sum of an iterable of numbers

    numbers: any iterable

    Return value: integer
    '''
    return sum(numbers)

def is_in(needle: int, haystack: List[Union[int, str]]) -> bool:
    '''
    Checks if the given item is in a list

    Parameters:
    - needle: a string or an integer
    - haystack: a list of strings or integers

    Return value: bool - if the needle is in the haystack
    '''
    return needle in haystack

def index_of_number(item: int, numbers: List[int]) -> Optional[int]:
    '''
    Returns the index of the given item in a list of numbers

    Parameters:
    - item: an integer
    - numbers: a list of numbers

    Return value: the index of the item, or None if the items is not in numbers
    '''
    if item in numbers:
        return numbers.index(item)
    return None
