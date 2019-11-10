# import itertools

# def powerset(l):
# 	if not l:
# 		return [[]]
# 	ps = powerset(l[1:])
# 	return ps + [[l[0]] + n for n in ps]

# def list_input():
# 	return list(map(int, input().strip().split(' ')))

# def substr(s):
#     l = []
#     for i in range(len(s) + 1):
#         for j in range(i+1, len(s) + 1):
#             l.append(s[i:j])
#     return l

# def perms(s):
#     return list(set([''.join(p) for p in itertools.permutations(s)]))
