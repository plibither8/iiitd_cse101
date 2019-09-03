def find_magic_num(x,y,z):
	"""This function returns the 'magic number' that is created
	after taking three numbers as input

	@params: Three floats
	Returns: (float) the magic number
	"""

	magic_num = ((x**2 + y) % z)**5
	return magic_num
