def rotate(string, direction, count):
	k = len(string)-count-1
	part_1 = string[0:count] if direction == 'left' else string[0:k]
	part_2 = string[count:] if direction == 'left' else string[k:]
	return(part_2 + part_1)

def fitin(tag, word):
	return(tag[0:2] + word + tag[2:])
