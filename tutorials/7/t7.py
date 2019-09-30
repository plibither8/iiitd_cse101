from math import ceil, factorial

# Q1
def q1():
	string = input()
	Vowel = list(map(lambda v: string.count(v), list('aeiou')))
	return Vowel

# Q2
def q2(A, N):
	sum = 0
	for i in range(N):
		sum += A[i] * (1 if i % 2 else -1)
	return sum

# Q3
def q3():
	n = int(input())

	for i in range(n):
		print(i + 1)
	print()

	for i in range(n):
		print('*' * (i+1))
	print()

	for i in range(n):
		start = int(i * (i + 1) / 2 + 1)
		print(''.join(map(str, list(range(start, start + i + 1)))))
	print()

	for i in range(n):
		print(' ' * (n - i - 1) + '*' * (i * 2 + 1))
	print()

	for i in range(n):
		print(' ' * (n - i - 1) + '*' * (i + 1))
	print()

	for i in range(n):
		print(' ' * (n - i - 1) + '*' * (i * 2 + 1))
	for i in range(n - 1)[::-1]:
		print(' ' * (n - i - 1) + '*' * (i * 2 + 1))
	print()

	for i in range(n):
		print('  ' * (n - i - 1) + '* ' * (i + 1))
	for i in range(n - 1)[::-1]:
		print('  ' * (n - i - 1) + '* ' * (i + 1))
	print()

	for i in range(n):
		print(' ' * i + '*' + ' ' * ((n - i - 1) * 2 - 1) + ceil((n - i - 1) / n) * '*')
	for i in range(n - 1):
		print(' ' * (n - i - 2) + '*' + ' ' * ((i + 1) * 2 - 1) + '*')
	print()

	def c(n, k):
		return int(factorial(n) / factorial(k) / factorial(n - k))

	for i in range(n):
		print(' '.join(map(str, map(lambda j: c(i, j), range(i + 1)))))
