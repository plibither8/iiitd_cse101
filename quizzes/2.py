print(nested_lst[2][2][1][1].x)

print(dict['k1']['k2']['n3'])

dict['k1']['k2']['n4'] = 40

map(lambda n: '_'.join(n.strip().split(' ')[::-1]), names)

def isPrime(n):
    if n is 0 or n is 1: return False
    for i in range(2, n):
        if n % i is 0: return False
    return True

print(list(filter(isPrime, ints)))

def common(lst1, lst2):
    return list(filter(lambda e: e in lst2, lst1))

