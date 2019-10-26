import json
import math
import os
import random
import re
import sys

#
# Complete the 'Nested_sum' function below.
#
# The function is expected to return an INTEGER.
# The function accepts STRING num_list as parameter.
#


def Nested_sum(num_list):
    # Write your code here
    final_sum = 0
    num_list = json.load(num_list)
    for i in num_list:
        if type(i) == type([]):
            final_sum = final_sum + Nested_sum(i)
        elif type(i) == type(4):
            final_sum = final_sum + i
    return final_sum


if __name__ == '__main__':
    num_list = input()

    result = Nested_sum(num_list)
    print(result)