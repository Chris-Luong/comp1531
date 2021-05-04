'''
NOTE: This exercise assumes you have completed divisors.py
'''

from divisors import divisors

# You may find this helpful
def is_prime(n):
    return n != 1 and divisors(n) == {1, n}

def factors(n):
    '''
    A generator that generates the prime factors of n. For example
    >>> list(factors(12))
    [2,2,3]

    Params:
      n (int): The operand

    Yields:
      (int): All the prime factors of n in ascending order.

    Raises:
      ValueError: When n is <= 1.
    '''
	'''
	need to remove this section for it to work
    if type(n) is not int or n <= 1:
      raise ValueError("Prime numbers are numbers greater than 1")

    i = 2
    while i <= n:
      if is_prime(i) and n % i == 0:
        n /= i
        yield i
      else:
        i += 1
	'''
    if type(n) is not int or n <= 1: # Some student tests expect type checking, so adding it here.
        raise ValueError(f"{n} does not have prime factors")
    for f in sorted(divisors(n)):
        if n == 1:
            break
        if is_prime(f):
            while n != 1 and n % f == 0:
                yield f
                n = n // f

