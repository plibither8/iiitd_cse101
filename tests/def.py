import itertools

n = int(input())
tests = []


def p(s):
    return s == s[::-1]


for i in range(n):
    a, b = input().strip().split(" ")
    a = int(a)
    tests.append((a, b))

for t in tests:
    k, s = t
    n = len(s)
    ss = []
    for i in range(n-k, n+1):
        a = list(itertools.combinations(s, i))
        a = list(map(lambda x: "".join(list(x)), a))
        ss += a
    print(ss)
    l = list(filter(lambda x: len(x) >= len(s)-k, ss))
    print(l)
    l = list(filter(p, l))
    print(l)
    if not l:
        print("NO")
    else:
        print("YES")

