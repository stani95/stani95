import matplotlib.pyplot as plt

def gcd(m,n):
	r = 1
	a = max(m,n)
	b = min(m,n)
	while r != 0:
		r = a % b
		a = b
		b = r
	return a

def phi(n):
	count = 0
	for i in range(1, n+1):
		if gcd(n, i) == 1:
			count += 1
	return count

size = 10000

x_axis = [i for i in range(1, size+1)]
y_axis = [phi(i) for i in range(1, size+1)]

plt.plot(x_axis, y_axis, 'o', markersize=1)
plt.show()
