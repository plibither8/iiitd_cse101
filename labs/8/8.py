
def kthLadder(N, K):
    return help_recursion(N)[K-1]

#
# Complete the 'help_recursion' function below.
#
# The function is expected to return a STRING.
# The function accepts INTEGER N as parameter.
#


def help_recursion(N):
    if N is 1:
        return "0"
    return "".join(list(map(lambda x: "01" if x is "0" else "10", list(help_recursion(N-1)))))


def maxDistract(C1, C2, H1, H2, M):
    a = M // C1 * H1
    b = M // C2 * H2

    if (a <= 0 and b <= 0):
        return 0

    if (a > b):
        return H1 + maxDistract(C1, C2, H1, H2, M - C1)
    if (b > a):
        return H2 + maxDistract(C1, C2, H1, H2, M - C2)

    if (C1 < C2):
        return H1 + maxDistract(C1, C2, H1, H2, M - C1)
    else:
        return H2 + maxDistract(C1, C2, H1, H2, M - C2)


maxDistract(2, 3, 3, 7, 20)
