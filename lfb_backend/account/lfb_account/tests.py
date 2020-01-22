from django.test import TestCase

# Create your tests here.


import re
import itertools


def solve(puzzle):
    print(puzzle)
    words = re.findall(r'[A-Z]+', puzzle.upper())
    print(words)
    unique_characters = set(''.join(words))
    assert len(unique_characters) <= 10, 'Too many letters'
    first_letters = {word[0] for word in words}
    n = len(first_letters)
    sorted_characters = ''.join(first_letters) + ''.join(unique_characters - first_letters)
    characters = tuple(ord(c) for c in sorted_characters)
    digits = tuple(ord(c) for c in '0123456789')
    zero = digits[0]
    print(len(characters))
    for guess in itertools.permutations(digits, len(characters)):
        if zero not in guess[:n]:
            print(puzzle, guess)
            equation = puzzle.translate(dict(zip(characters, guess)))
            print(equation)
            if eval(equation):
                return equation


if __name__ == '__main__':
    puzzle = 'I + LOVE + YOU == DORA'
    print(solve(puzzle))
    # print(solve(puzzle))
    # print(re.findall('[A-Z]+', puzzle.upper()))