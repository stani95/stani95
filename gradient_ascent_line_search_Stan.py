import matplotlib.pyplot as plt
import numpy as np
import math

#The area as a function of b, theta, and W.
def A(b,theta,W):
	sin_theta = math.sin(theta)
	cos_theta = math.cos(theta)
	return 0.25*(W-b)*sin_theta*(2*b+(W-b)*cos_theta)

#For plotting purposes:
A2 = np.vectorize(A)

#The partial derivative of A with respect to b:
def A_der_b(b,theta,W):
	sin_theta = math.sin(theta)
	cos_theta = math.cos(theta)
	return 0.5*sin_theta*(W-2*b-W*cos_theta+b*cos_theta)

#The partial derivative of A with respect to theta:
def A_der_theta(b,theta,W):
	sin_theta = math.sin(theta)
	cos_theta = math.cos(theta)
	return 0.25*(W-b)*(2*b*cos_theta+(W-b)*(2*cos_theta*cos_theta-1))

#This function helps us find a value for alpha which gives a negative value of the derivative,
#so we can initiate the bisection algorithm using that value:
def find_negative(h_prime):

	#This should never happen because when following the gradient direction,
	#we should be clumbing up:
	if h_prime(0) < 0:
		print "ERROR"
		print "The value", h_prime(0), "should be positive and it is not!!!"

	#If that happens, we can pass it to the bissection algorithm directly
	elif h_prime(0) == 0:
		return 0

	#The main case. Trying alpha=1 and doubling at each step until we find the desired value:
	else:
		if h_prime(1) < 0:
			return 1
		current_value = 1.0
		check_if_negative = 1
		while check_if_negative > 0:
			current_value = 2*current_value
			check_if_negative = h_prime(current_value)
		return current_value

#The bisection algorithm:
#This function finds a zero of the derivative of the function of alpha
#that we need to optimize for the line search
def bisection(h_prime):

	right_end = find_negative(h_prime)

	#If the derivative is zero for alpha=0:
	if right_end==0:
		return 0.

	found_zero = False
	left_end = 0.0
	while True:

		#If the derivative at the midpoint is positive, we can move the left end there:
		if h_prime((right_end + left_end)/2.0) > 0.0001:
			left_end = (right_end + left_end)/2.0

		#If the derivative at the midpoint is negative, we can move the right end there:
		elif h_prime((right_end + left_end)/2.0) < -0.0001:
			right_end = (right_end + left_end)/2.0

		#If we get (sufficiently close to) zero, return the point:
		else:
			return (right_end + left_end)/2.0

# The gradient ascent with line search algorithm:
def gradient_descent(A,A_der_b,A_der_theta,b_current,theta_current,W):

	#I am comparing the new function value with the previous one,
	#and I stop the algorithm once they become equal (no improvement)
	old_max = 0.
	new_max = 1.
	first_iteration = True

	#The main loop of the gradient ascent algorithm
	while old_max<new_max:

		#Computing the derivative of the function of alpha we need to optimize for the line search:
		def h_alpha(alpha):

			#The partial derivative of A with respect to b evaluated at the current point:
			f_b = A_der_b(b_current,theta_current,W)

			#The partial derivative of A with respect to theta evaluated at the current point:
			f_theta = A_der_theta(b_current,theta_current,W)

			Sin = math.sin(theta_current+alpha*f_theta)
			Cos = math.cos(theta_current+alpha*f_theta)
			B = b_current+alpha*f_b

			return (-0.25*f_b)*Sin*((2-Cos)*B+W*Cos)+(0.25*(W-B))*(Cos*f_theta)*((2-Cos)*B+W*Cos)+(0.25*(W-B))*Sin*(Sin*f_theta*B+(2-Cos)*f_b-W*Sin*f_theta)

		#Applying the bisection algorithm to that function to find the optimal value of alpha :) :
		alpha = bisection(h_alpha)

		#Computing the updated values for b and theta:
		next_value_b = b_current + A_der_b(b_current,theta_current,W)*alpha
		next_value_theta = theta_current + A_der_theta(b_current,theta_current,W)*alpha

		#Plotting the line from the old value to the new value:
		plt.plot((b_current,next_value_b),(theta_current,next_value_theta), "black")

		#Updating the vablues of b and theta:
		b_current = next_value_b
		theta_current = next_value_theta

		#Updating and printing the function values:
		old_max = new_max
		new_max = A(next_value_b,next_value_theta,W)
		print new_max

		#We do not have an old_max during the first iteration:
		if first_iteration:
			old_max = new_max-1.
			first_iteration = False

	#Returning the coordinates of the local maximum:
	return (next_value_b, next_value_theta)


#Executing and Plotting:
b_list = np.linspace(0., 3.0, 2000)
theta_list = np.linspace(0., math.pi*0.5, 2000)
b, theta = np.meshgrid(b_list, theta_list)
area = A2(b,theta,3.0)

plt.figure()
contour_plot = plt.contour(b, theta, area, [0,0.2,0.4,0.6,0.8,1.,1.12,1.2,1.25,1.282,1.295,1.299])
plt.clabel(contour_plot, fontsize=8, inline_spacing=0)

plt.xlabel("b")
plt.ylabel("theta")
plt.title("Gradient ascent with exact line search")

plt.axes().set_aspect('equal')

answer = gradient_descent(A,A_der_b,A_der_theta,2.99,0.01,3.0)
print "The local maximum is achieved at the point:", answer

plt.show()
