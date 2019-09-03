def find_magic_num(x,y,z):
	"""This function returns the 'magic number' that is created
	after taking three numbers as input

	@params: Three floats
	Returns: (float) the magic number
	"""

	magic_num = ((x**2 + y) % z)**5
	return magic_num

print('Enter three numbers to find the magic number:')
x = float(input())
y = float(input())
z = float(input())

print(find_magic_num(x, y, z))
