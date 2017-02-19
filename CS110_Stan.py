import random
import matplotlib.pyplot as plt
import math

#This function takes as input the size of the square and the number of darts, and returns the estimate of pi and the associated error. 
def standard_dartboard(S, N):
	miss = 0
	#I count the number of misses.
	for i in range (N):
		#These are the two coordinates of the chosen point.
		a = random.randint(-S, S)
		b = random.randint(-S, S)
		#This checks if the point lies inside of the circle.
		if math.sqrt(a**2 + b**2)>S:
			#Increase the number of misses if it lies outside of the circle.
			miss += 1

	#The number of shots made equals the total number of darts minus the number of misses.
	made = N - miss
	#To get the estimate of pi from the ratio of made and N, we have to multiply by 4.
	pi_estimate = float(4*made)/float(N)
	#The error equals the estimate minus the true value of pi. It can be positive or negative.
	error_pi = pi_estimate-math.pi
	#The function returns the estimate of pi and the associated error.
	return pi_estimate, error_pi


#We will store the upper limit of the error bars in this variable.
error_up_pi=[]

#We will store the lower limit of the error bars in this variable.
error_down_pi=[]

#We will store the number of estimates that lie outside of the error bars in this variable.
bad=0

#These are all the estimates made.
alll=0

#We will store the list of estimates of pi in this variable.
results=[]

#This is the range of values of N.
ran = range(10, 3000)

for i in ran:
	#result[0] has the current estimate of pi, and result[1] has the associated error. The radius of the circle is 500 000.
	result = standard_dartboard(500000, i)
	results.append(result[0])

	#This constant contains the mathematical expression that we need to determine the error bars.
	error_constant = 4*1.96*math.sqrt((math.pi/4.0)*(1-math.pi/4.0))

	#To construct the theoretical error bars, add pi to the error from the formula.
	error_up_pi.append(float(error_constant)/float(math.sqrt(i))+math.pi)
	error_down_pi.append(-float(error_constant)/float(math.sqrt(i))+math.pi)

	alll+=1
	if result[1]>float(error_constant)/float(math.sqrt(i)) or result[1]<-float(error_constant)/float(math.sqrt(i)):
		#If the absolute value of the error turns out to be more than the absolute value of the error bar, increment the number of bad samples.
		bad+=1

	print i


print "Estimations outside of the error bars: ", float(bad)/float(alll), " (expected ~0.05)"
print "Pi equals ", result[0]


plt.plot(ran, results, color = "RED")
plt.plot(ran, error_up_pi, color = "BLUE")
plt.plot(ran, error_down_pi, color = "BLUE")
plt.plot(ran, [math.pi]*len(ran), color = "BLACK")
plt.xlabel('Number of darts')
plt.ylabel('Estimate for pi')
plt.title('Change in the estimation of pi with increasing number of darts')
plt.show()
