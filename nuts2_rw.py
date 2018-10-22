#Imports:
import math
import random
from scipy.stats import norm

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

#Seeds:
random.seed(3)
np.random.seed(3)

#----------------------------

# The distribution to sample from:
def sigmoid(x):
	result=[]
	if isinstance(x,np.float64) or isinstance(x,float):
		return 1./(1+math.exp(-x))
	t = 0
	for i in x:
		result.append([])
		for j in i:
			result[t].append(1./(1+math.exp(-j)))
		t += 1
	return np.array(result)

def distr(theta, alpha):
	r = 1
	c1 = -4
	c2 = 3
	likelihood = np.exp(np.log(norm.pdf(-5.5, theta, 4))+np.log(norm.pdf(-4.3, theta, 4))+np.log(norm.pdf(-2, theta, 4))+np.log(norm.pdf(-1.2, theta, 4))+np.log(norm.pdf(-1, theta, 4))+np.log(norm.pdf(-0.5, theta, 4))+np.log(norm.pdf(1, theta, 4)))
	prior = sigmoid(alpha)*norm.pdf(theta, c1,r) + (1-sigmoid(alpha))*norm.pdf(theta, c2,r)
	hyperprior = norm.pdf(alpha,0,2)
	return likelihood*prior*hyperprior

#----------------------------

# The negative log of the distribution to sample from:
def logdistr(x, y):
	result=[]
	if isinstance(distr(x,y),np.float64):
		return -math.log(distr(x,y))
	t = 0
	for i in distr(x,y):
		result.append([])
		for j in i:
			result[t].append(-math.log(j))
		t += 1
	return np.array(result)

#----------------------------

#Plot of the distribution to sample from:
fig = plt.figure()
ax = fig.gca(projection='3d')
x = np.arange(-6, 6, 0.05)
y = np.arange(-8, 8, 0.05)
x, y = np.meshgrid(x, y)
surf = ax.plot_surface(x, y, distr(x,y), cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.set_xlabel('theta')
ax.set_ylabel('alpha')
plt.show()

#----------------------------

#Plot of the negative log of the distribution to sample from:
fig = plt.figure()
ax = fig.gca(projection='3d')
x = np.arange(-6, 6, 0.05)
y = np.arange(-8, 8, 0.05)
x, y = np.meshgrid(x, y)
surf2 = ax.plot_surface(x, y, logdistr(x,y), cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.set_xlabel('theta')
ax.set_ylabel('alpha')
plt.show()

#----------------------------

#Calculates the x-gradient of a function at a point.
def deriv_x(distr, point, epsilon):
	return (distr(point[0]+epsilon*0.5,point[1])-distr(point[0]-epsilon*0.5,point[1]))/float(epsilon)

#Calculates the y-gradient of a function at a point.
def deriv_y(distr, point, epsilon):
	return (distr(point[0],point[1]+epsilon*0.5)-distr(point[0],point[1]-epsilon*0.5))/float(epsilon)

#The leapfrog integrator:
def leapfrog(distr, i_pos, i_mom, num_steps, eps):
	eps_for_deriv = 0.000001
	positions = [i_pos]
	momenta = [i_mom]
	for i in range(num_steps):
        #Leapfrog equation 1:
		interm_mom = [i_mom[0] - 0.5*eps*deriv_x(distr, i_pos, eps_for_deriv), i_mom[1] - 0.5*eps*deriv_y(distr, i_pos, eps_for_deriv)]
        #Leapfrog equation 2:
		f_pos = [i_pos[0] + eps*interm_mom[0], i_pos[1] + eps*interm_mom[1]]
        #Leapfrog equation 3:
		f_mom = [interm_mom[0] - 0.5*eps*deriv_x(distr, f_pos, eps_for_deriv), interm_mom[1] - 0.5*eps*deriv_y(distr, f_pos, eps_for_deriv)]
		i_pos = f_pos
		i_mom=f_mom
		positions.append(f_pos)
		momenta.append(f_mom)
	#returns a list of all positions and all momenta in the sequence (for NUTS, we only need to do one step at a time, so it returns only the initial and the final position and momentum)
	return positions, momenta

#----------------------------

#For NUTS, the initial momentum is sampled from a standard Gaussian with identity covariance matrix, thus kick_strength=1.
kick_strength = 1.

#Choosing the initial position:
initial_pos = [20*(random.random()-0.25), 20*(random.random()-0.25)]
print ("Initial position is:", initial_pos)

#The number of samples we want:
num_samples = 5000

#The value for epsilon, the length of a leapfrog step (needs tuning in this implementation):
epsil = 0.5

#----------------------------

#NUTS:

'''
The BuildTree function:

Takes as input a position-momentum state, a direction v=+1 or v=-1, a depth j, and the values for u and epsilon.

Returns:
{position_minus, momentum_minus, position_plus, momentum_plus (the leftmost and rightmost state of the built tree),
C' (the elements to be added to C from the built tree), s' (stopping condition: 0 if we need to stop doubling)}
'''

def BuildTree(position, momentum, u_variable, v_direction, j_depth, e_stepsize, logdistr):

	#Base case
	if j_depth==0:

		#Do a leapfrog step in the specified direction:
		leapfrog_result = leapfrog(logdistr, position, momentum, 1, v_direction*e_stepsize)
		#The new position and momentum after the leapfrog step:
		position_prime = leapfrog_result[0][-1]
		momentum_prime = leapfrog_result[1][-1]

		C_prime = []
		if u_variable <= math.exp(-logdistr(*position_prime)-(sum([x1*y1 for x1,y1 in zip(momentum_prime,momentum_prime)])*0.5)):
			#We can add this state to C only if it satisfies the condition that the density at that point is larger than u.
			C_prime.append([position_prime, momentum_prime])

		#Check for large numerical errors and stop doubling if encountered:
		s_prime = 1 if u < math.exp(100.-logdistr(*position_prime)-(sum([x1*y1 for x1,y1 in zip(momentum_prime,momentum_prime)])*0.5)) else 0

		return position_prime, momentum_prime, position_prime, momentum_prime, C_prime, s_prime

	#Recursive case (j>0):
	else:
		#Building the first subtree in the specified direction (by v) with the specified size (by j_depth-1):
		pos_m, mom_m, pos_p, mom_p, C_prime, s_prime = BuildTree(position, momentum, u_variable, v_direction, j_depth-1, e_stepsize, logdistr)

		#Building the second subtree in the specified direction (by v) with the specified size (by j_depth-1):
		if v_direction == -1:
			#If direction is to the left (v=-1), then we use the leftmost state (pos_m, mom_m) to begin building the second subtree:
			result = BuildTree(pos_m, mom_m, u_variable, v_direction, j_depth-1, e_stepsize, logdistr)
			#We only take the leftmost state of the second tree and later use it to check for a U-turn between it and the rightmost one
			pos_m, mom_m, C_sec, s_sec = result[:2]+result[4:]

		else:
			#If direction is to the right (v=1), then we use the rightmost state (pos_p, mom_p) to begin building the second subtree:
			result = BuildTree(pos_p, mom_p, u_variable, v_direction, j_depth-1, e_stepsize, logdistr)
			#We only take the rightmost state of the second tree and later use it to check for a U-turn between it and the leftmost one
			pos_p, mom_p, C_sec, s_sec = result[2:]

		#Check for a U-turn. It takes into account all pairs of states that are leftmost-rightmost for any balanced subtree.
		s_prime = s_prime*s_sec*( 1 if sum([x1*y1 for x1,y1 in zip([xx-yy for xx,yy in zip(pos_p,pos_m)],mom_m)]) >= 0 else 0 )*( 1 if sum([x1*y1 for x1,y1 in zip([xx-yy for xx,yy in zip(pos_p,pos_m)],mom_p)])>=0 else 0 )

		#Add the newly admitted states to C into one set C to return:
		C_prime = C_prime + C_sec

		return pos_m, mom_m, pos_p, mom_p, C_prime, s_prime

#----------------------------

#We record the set of samples here:
samples = []

#We need this many samples:
for m in range(num_samples):

	#Setting up the initial momentum:
	initial_mom = [np.random.normal(0,kick_strength), np.random.normal(0,kick_strength)]

	#Sampling u:
	u = random.random()*math.exp(-logdistr(*initial_pos)-(sum([x1*y1 for x1,y1 in zip(initial_mom,initial_mom)])*0.5))

	pos_m = initial_pos
	pos_p = initial_pos
	mom_m = initial_mom
	mom_p = initial_mom
	j = 0
	C = [[initial_pos, initial_mom]]
	s = 1

	#While the stopping condition is not satisfied, continue building the tree:
	while s == 1:

		#Sampling a direction:
		v = -1
		if random.random()<0.4:
			v = 1

		if v == -1:
			#If the direction is to the left, build a subtree to the left, starting from (pos_m, mom_m).
			result = BuildTree(pos_m, mom_m, u, v, j, epsil, logdistr)

			#We only take the leftmost states:
			pos_m, mom_m, C_prime, s_prime = result[:2]+result[4:]

		else:
			#If the direction is to the right, build a subtree to the right, starting from (pos_p, mom_p).
			result = BuildTree(pos_p, mom_p, u, v, j, epsil, logdistr)

			#We only take the rightmost states:
			pos_p, mom_p, C_prime, s_prime = result[2:]

		if s_prime == 1:
			#We only append the new candidate states for C into C, if no stopping condition has been met within the newly built subtree. Otherwise, we ignore the states from the last tree that weas built.
			C = C + C_prime

		#We check for whether the leftmost and rightmost state of the full tree make a U-turn:
		s = s_prime*( 1 if sum([x1*y1 for x1,y1 in zip([xx-yy for xx,yy in zip(pos_p,pos_m)],mom_m)]) >= 0 else 0 ) * ( 1 if sum([x1*y1 for x1,y1 in zip([xx-yy for xx,yy in zip(pos_p,pos_m)],mom_p)])>=0 else 0 )

		#Increasing the depth of the tree fot the next iteration:
		j += 1

	#Sampling the desired state uniformly from the states in C:
	sample_index = np.random.random_integers(0,len(C)-1)
	samples.append( C[sample_index] )

	#Use this new sampled state as the new initial position:
	initial_pos = samples[-1][0]

#----------------------------

samples = [i[0] for i in samples]
samples_x = [i[0] for i in samples]
samples_y = [i[1] for i in samples]

print ("FINAL SAMPLES =", samples)

#----------------------------

y_list = []
for i in samples:
	y_list.append(logdistr(*i)+0.2)

#A plot of how the samples look like in the context of the negative-log distribution:
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.arange(-6, 6, 0.05)
y = np.arange(-8, 8, 0.05)
x, y = np.meshgrid(x, y)
ax.plot_wireframe(x, y, logdistr(x,y), cmap=cm.coolwarm, linewidth=0.5, antialiased=False)
ax.scatter(samples_x, samples_y, y_list, c='r')
ax.set_xlabel('theta')
ax.set_ylabel('alpha')
plt.show()

#A histogram of the samples in the context of the target distribution:
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = np.arange(-6, 6, 0.05)
y = np.arange(-8, 8, 0.05)
x, y = np.meshgrid(x, y)

hist, xedges, yedges = np.histogram2d(samples_x, samples_y, bins=20, range=[[-6, 6], [-8, 8]], normed = True)
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25, indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0
dx = dy = 0.5 * np.ones_like(zpos)
dz = hist.ravel()

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='r', zsort='average')
ax.plot_wireframe(x, y, 200000000*distr(x,y), cmap=cm.coolwarm, linewidth=1., antialiased=False)
ax.set_xlabel('theta')
ax.set_ylabel('alpha')

plt.show()
