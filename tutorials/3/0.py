def quad_roots(a, b, c):
	d = (b**2 - 4*a*c)**0.5
	return((-b + d) / 2, (-b - d) / 2)


def main():
	print("Enter the three coeffs: ")
	coeffs = map(float, input().split()) 
	roots = quad_roots(*coeffs)
	print(*roots)

if __name__ == "__main__":
	main()