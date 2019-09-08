# Problem 1
def fix_teen(n):
	return 0 if (19 >= n > 16 or 15 > n >= 13) else n

def no_teen_sum(a, b, c):
	return sum(map(fix_teen, [a, b, c]))

# Problem 3
def return_grade(grade):
	if 0 <= grade <= 45:
		return 'F'
	if grade <= 60:
		return 'D'
	if grade <= 75:
		return 'C'
	if grade <= 90:
		return 'B'
	return 'A'

# Problem 4
def str_concat(S, K):
	P = K if K % 3 is 0 or K % 5 is 0 and K % 15 is not 0 else 0
	return S * P

# Problem 5