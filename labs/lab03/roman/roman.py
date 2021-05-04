def roman(numerals):
    '''
    Given Roman numerals as a string, return their value as an integer. You may
    assume the Roman numerals are in the "standard" form, i.e. any digits
    involving 4 and 9 will always appear in the subtractive form.

    For example:
    >>> roman("II")
    2
    >>> roman("IV")
    4
    >>> roman("IX")
    9
    >>> roman("XIX")
    19
    >>> roman("XX")
    20
    >>> roman("MDCCLXXVI")
    1776
    >>> roman("MMXIX")
    2019
    '''
    i = 0
    result = 0
    roman = {'I': 1, 'IV': 4, 'V': 5,
            'IX': 9, 'X': 10, 'XL': 40,
            'L': 50, 'XC': 90, 'C': 100,
            'CD': 400, 'D': 500, 'CM': 900,
            'M': 1000
    }

    while i < len(numerals):
        if i + 1 < len(numerals) and numerals[i:i+2] in roman:
            result += roman[numerals[i:i+2]]
            i += 2
        else:
            result += roman[numerals[i]]
            i += 1
    
    return result