# Task 1
def get_every_fourth(S):
	S = S.strip()
	return S[::-4][::-1]

# Task 2
def get_every_kth(S, k, i):
	S = S.strip()
	return S[:i+1][::-1][::k][::-1]

# Task 3
def decode_string(S):
	S = S.strip()
	return S[::-1][S.find('_') + 1:S.find('_', S.find('_') + 1)][::-1]
