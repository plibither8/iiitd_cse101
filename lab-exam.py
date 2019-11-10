#!/bin/python3

import math
import os
import random
import re
import sys


class Matrix:
    def __str__(self):
        s = ' '.join([str(elem) for elem in self.arr])
        return s

    def set_element(self, a, x, y):
        self.arr[x][y] = a

    def __add__(self, value):
        result = Matrix(self.m, self.n, [[0] * self.n for _ in range(self.m)])
        for i in range(self.m):
            for j in range(self.n):
                v = self.arr[i][j] + value.arr[i][j]
                result.set_element(v, i, j)
        return result

    def __sub__(self, value):
        result = Matrix(self.m, self.n, [[0] * self.n for _ in range(self.m)])
        for i in range(self.m):
            for j in range(self.n):
                v = self.arr[i][j] - value.arr[i][j]
                result.set_element(v, i, j)
        return result

    def __mul__(self, value):
        result = Matrix(self.n, self.m, [[0] * self.m for _ in range(self.n)])
        for i in range(self.m):
            for j in range(self.n):
                v = 0
                for k in range(self.n):
                    v += self.arr[i][k] * value.arr[k][j]
                    print(v)
                result.set_element(v, j, i)
        return result

    def __init__(self, m, n, arr):
        self.m = m
        self.n = n
        self.arr = arr


if __name__ == '__main__':
    s = input()

    print(eval(s))
