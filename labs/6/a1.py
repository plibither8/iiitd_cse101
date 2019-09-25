from math import sqrt

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Line:
	def __init__(self,a,b,c):
		self.a = a
		self.b = b
		self.c = c

class Circle:
	def __init__(self,centre_x,centre_y,radius):
		self.centre_x = centre_x
		self.centre_y = centre_y
		self.radius = radius


def findMirrorPoint(p, l):
	x_coord = (p.x*(l.a**2 - l.b**2) - 2*l.b*(l.a*p.y + l.c)) / (l.a**2 + l.b**2)
	y_coord = (p.y*(l.b**2 - l.a**2) - 2*l.a*(l.b*p.x + l.c)) / (l.a**2 + l.b**2)
	p.x = x_coord
	p.y = y_coord

def checkSides(p1, p2, l1, l2):
	findMirrorPoint(p1, l1)
	term1 = l2.a*p1.x + l2.b*p1.y + l2.c
	term2 = l2.a*p2.x + l2.b*p2.y + l2.c

	return term1 * term2 > 0

def checkIntersection(c1, c2):
	dist = sqrt((c1.centre_x - c2.centre_x)**2 + (c1.centre_y - c2.centre_y)**2)
	return dist <= c1.radius + c2.radius and dist >= abs(c1.radius - c2.radius)

