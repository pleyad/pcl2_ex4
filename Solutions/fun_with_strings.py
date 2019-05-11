#!/usr/bin/env python3
# coding: utf8

from typing import Iterable


def longest_substrings(x: str, y: str) -> Iterable[str]:
    '''Returns the longest common substrings of two strings.'''

    x = x.lower()
    y = y.lower()

    n, m = len(x), len(y)

    maxlength = 0
    x_coordinates = []

    #  Matrix
    d = [[None for _ in range(m+1)] for _ in range(n+1)]

    # Initialize top row and leftmost column
    for i in range(n+1):
        d[i][0] = 0
    for j in range(m+1):
        d[0][j] = 0

    # Calculate the rest
    for i in range(1, n+1):
        for j in range(1, m+1):
            if x[i-1] == y[j-1]:
                d[i][j] = d[i-1][j-1] + 1

                # Remember the end of the currently longest substring
                if d[i][j] == maxlength:
                    x_coordinates.append(i)
                elif d[i][j] > maxlength:
                    maxlength = d[i][j]
                    x_coordinates = [i]
            else:
                d[i][j] = 0

    longest_substrings = []

    for c in x_coordinates:
        substring = x[c-maxlength:c]
        longest_substrings.append(substring)

    # Visualization
    '''y = '0'+y
    x = '0'+x
    print('  {}'.format(y))
    for i in range(n+1):
        print(' ')
        print('{} {}'.format(x[i], ' '.join([str(x) for x in d[i]])))
    '''
    return set(longest_substrings)
