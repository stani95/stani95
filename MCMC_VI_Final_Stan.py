
'''
The current variational parameters
are NOT optimized. Uncomment one of the
gradient ascent chuncks of code below to
optimize them.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
np.random.seed(1)

#SIMULATION ONLY WORKS FOR num_points = 5!
num_points = 5

#Generating data:
data_Ax = np.random.normal(0,2.,num_points)
data_Ay = np.random.normal(0,10.,num_points)
data_A = np.array(list(zip(data_Ax, data_Ay)))

data_Bx = np.random.normal(0,10.,num_points)
data_By = np.random.normal(0,1.,num_points)
data_B = np.array(list(zip(data_Bx, data_By)))

data = np.concatenate((data_A,data_B))

#The likelihood function:
def a_2d_zero_centered_gaussian(x, theta):
	theta_var = [0.,0.]
	theta_var[0] = theta[0]**2    #Converting standard deviation to variance
	theta_var[1] = theta[1]**2
	return (1/(2*np.pi*np.sqrt(theta_var[0]*theta_var[1])))*np.exp(-0.5*(((x[0])**2)/(theta_var[0])+((x[1])**2)/(theta_var[1])))

#The derivative of the hyperbolic tangent function:
def tanh_der(x):
	return 4./(np.exp(x)+np.exp(-x))**2

#For transforming u, such that w^Tu >= -1, so the transformation f is invertible:
def m(x):
	return -1.+np.log(1.+np.exp(x))

#The initial variational approximation:
def q_density(x, mu, sigma):
	sigma_var = [0.,0.]
	sigma_var[0] = sigma[0]**2    #Converting standard deviation to variance
	sigma_var[1] = sigma[1]**2
	return (1/(2*np.pi*np.sqrt(sigma_var[0]*sigma_var[1])))*np.exp(-0.5*(((x[0]-mu[0])**2)/(sigma_var[0])+((x[1]-mu[1])**2)/(sigma_var[1])))

#Log of the initial variational approximation:
def log_q_density(x, mu, sigma):
	sigma_var = [0.,0.]
	sigma_var[0] = sigma[0]**2    #Converting standard deviation to variance
	sigma_var[1] = sigma[1]**2
	return np.log((1/(2*np.pi*np.sqrt(sigma_var[0]*sigma_var[1])))*np.exp(-0.5*(((x[0]-mu[0])**2)/(sigma_var[0])+((x[1]-mu[1])**2)/(sigma_var[1]))))

#The unnormalized posterior:
def get_unnormalized_density(theta, data):
	my_log = 0.
	for i in data:
		my_log += np.log(a_2d_zero_centered_gaussian(i,theta))
	return np.exp(my_log)*1e30

#See Appendix 1, pages 17 and 23 for these definitions:
def kappa(s,sigma,mu,w,b):
	return np.dot(w,s*sigma+mu)+b

def alpha(kappa):
	return np.exp(kappa)+np.exp(-kappa)

def beta(w,s,alpha):
	return 4*w*s/((alpha)**2)

def delta(s,sigma,mu,kappa,u):
	return s*sigma+mu+np.tanh(kappa*u)

def gamma(s,u,beta,delta):
	return (s+u*beta)/delta

def rho(u,beta,delta):
	return (u/delta)*np.array([beta[1],beta[0]])

def tau(s,sigma,mu):
	return s*sigma+mu

#Calculates the sum of squares of the data for each coordinate.
#It turns out this is a sufficient statistic.
def sum_my_sq(data):
	return [sum([i**2 for i in data[:,0]]),sum([i**2 for i in data[:,1]])]

#See Appendix 1, page 21 for the derivations of these:
def gradient_of_u_1_wrt_w_1(u_arbitrary, w):
	return (-1+np.log(1+np.exp(np.dot(w,u_arbitrary)))-np.dot(w,u_arbitrary))/(w[0]**2+w[1]**2)+w[0]*(((u_arbitrary[0])/(1+np.exp(np.dot(w,u_arbitrary)))-u_arbitrary[0])*(w[0]**2+w[1]**2)-2.*w[0]*(-1.+np.log(1+np.exp(np.dot(w,u_arbitrary)))-np.dot(w,u_arbitrary)))/((w[0]**2+w[1]**2)**2)

def gradient_of_u_2_wrt_w_1(u_arbitrary, w):
	return w[1]*(((u_arbitrary[0])/(1+np.exp(np.dot(w,u_arbitrary)))-u_arbitrary[0])*(w[0]**2+w[1]**2)-2.*w[0]*(-1.+np.log(1+np.exp(np.dot(w,u_arbitrary)))-np.dot(w,u_arbitrary)))/((w[0]**2+w[1]**2)**2)

def gradient_of_u_1_wrt_w_2(u_arbitrary, w):
	return w[0]*(((u_arbitrary[1])/(1+np.exp(np.dot(w,u_arbitrary)))-u_arbitrary[1])*(w[0]**2+w[1]**2)-2.*w[1]*(-1.+np.log(1+np.exp(np.dot(w,u_arbitrary)))-np.dot(w,u_arbitrary)))/((w[0]**2+w[1]**2)**2)

def gradient_of_u_2_wrt_w_2(u_arbitrary, w):
	return (-1+np.log(1+np.exp(np.dot(w,u_arbitrary)))-np.dot(w,u_arbitrary))/(w[0]**2+w[1]**2)+w[1]*(((u_arbitrary[1])/(1+np.exp(np.dot(w,u_arbitrary)))-u_arbitrary[1])*(w[0]**2+w[1]**2)-2.*w[1]*(-1.+np.log(1+np.exp(np.dot(w,u_arbitrary)))-np.dot(w,u_arbitrary)))/((w[0]**2+w[1]**2)**2)

#See Appendix 1, page 17 for the definitions of these:
def gradient_of_my_ELBO_wrt_sigma_1(s, sigma, mu, u, w, b, sum_my_sq,gamma,delta,rho,kappa,alpha):
	return (1./sigma[0])-10.*gamma[0]-10*rho[1]+(gamma[0])/(delta[0]**2)*sum_my_sq[0]+(rho[1])/(delta[1]**2)*sum_my_sq[1]-(8*np.dot(u,w)*s[0]*w[0]*(np.exp(kappa)-np.exp(-kappa)))/(alpha**3+4*np.dot(u,w)*alpha)

def gradient_of_my_ELBO_wrt_sigma_2(s, sigma, mu, u, w, b, sum_my_sq,gamma,delta,rho,kappa,alpha):
	return (1./sigma[1])-10.*gamma[1]-10*rho[0]+(gamma[1])/(delta[1]**2)*sum_my_sq[1]+(rho[0])/(delta[0]**2)*sum_my_sq[0]-(8*np.dot(u,w)*s[1]*w[1]*(np.exp(kappa)-np.exp(-kappa)))/(alpha**3+4*np.dot(u,w)*alpha)

#See Appendix 1, page 20 for the definition of this:
def gradient_of_my_ELBO_wrt_b(s, sigma, mu, u, w, b, sum_my_sq,delta,rho,kappa,alpha):
	return -10.*((4.*u[0])/(delta[0]*(alpha**2))+(4.*u[1])/(delta[1]*(alpha**2)))+((4.*u[0])/((delta[0]**3)*(alpha**2)))*sum_my_sq[0]+((4.*u[1])/((delta[1]**3)*(alpha**2)))*sum_my_sq[1]-(8.*np.dot(u,w)*(np.exp(kappa)-np.exp(-kappa)))/(alpha**3+4.*alpha*np.dot(u,w))

#See Appendix 1, page 24 for the definitions of these:
def gradient_of_my_ELBO_wrt_w_1(s, sigma, mu, u, w, b, sum_my_sq,delta,kappa,alpha,tau,u_arbitrary):
	return -10.*(((4*u[0]*tau[0])/(alpha**2)+np.tanh(kappa)*gradient_of_u_1_wrt_w_1(u_arbitrary,w))/(delta[0])+(((4*u[1]*tau[0])/(alpha**2)+np.tanh(kappa)*gradient_of_u_2_wrt_w_1(u_arbitrary,w))/(delta[1])))+(((4*u[0]*tau[0])/(alpha**2)+np.tanh(kappa)*gradient_of_u_1_wrt_w_1(u_arbitrary,w))/(delta[0]**3))*sum_my_sq[0]+(((4*u[1]*tau[0])/(alpha**2)+np.tanh(kappa)*gradient_of_u_2_wrt_w_1(u_arbitrary,w))/(delta[1]**3))*sum_my_sq[1]+((-8.*np.dot(w,u))*((tau[0]*(np.exp(kappa)-np.exp(-kappa)))/alpha)+4.*(w[0]*gradient_of_u_1_wrt_w_1(u_arbitrary,w)+u[0]+w[1]*gradient_of_u_2_wrt_w_1(u_arbitrary,w)))/(alpha**2+4.*np.dot(w,u))

def gradient_of_my_ELBO_wrt_w_2(s, sigma, mu, u, w, b, sum_my_sq,delta,kappa,alpha,tau,u_arbitrary):
	return -10.*(((4*u[1]*tau[1])/(alpha**2)+np.tanh(kappa)*gradient_of_u_2_wrt_w_2(u_arbitrary,w))/(delta[1])+(((4*u[0]*tau[1])/(alpha**2)+np.tanh(kappa)*gradient_of_u_1_wrt_w_2(u_arbitrary,w))/(delta[0])))+(((4*u[1]*tau[1])/(alpha**2)+np.tanh(kappa)*gradient_of_u_2_wrt_w_2(u_arbitrary,w))/(delta[1]**3))*sum_my_sq[1]+(((4*u[0]*tau[1])/(alpha**2)+np.tanh(kappa)*gradient_of_u_1_wrt_w_2(u_arbitrary,w))/(delta[0]**3))*sum_my_sq[0]+((-8.*np.dot(w,u))*((tau[1]*(np.exp(kappa)-np.exp(-kappa)))/alpha)+4.*(w[1]*gradient_of_u_2_wrt_w_2(u_arbitrary,w)+u[1]+w[0]*gradient_of_u_1_wrt_w_2(u_arbitrary,w)))/(alpha**2+4.*np.dot(w,u))


#The numpy functions did not work for meshgrid variables
#for some reason, so I created my own functions:
def dot_product(theta,x):
	return theta[0]*x[0]+theta[1]*x[1]

def scalar_times_vector(theta,x):
	return np.array([theta*x[0],theta*x[1]])


#The function f() that transforms according to a planar flow:
def planar_transformation(theta,u,w,b):
	return np.array(theta)+scalar_times_vector(np.tanh(dot_product(theta,w)+b),u)

#The psi here is different from the psi in my paper and is based on the psi in Rezende & Mohamed (2016):
def psi(theta,w,b):
	return scalar_times_vector(tanh_der(dot_product(theta,w)+b),w)

#The log-density of the transformed variational approximation:
def log_planar_flow(theta, u, w, b, mu, sigma):
	return log_q_density(theta, mu,sigma) - np.log(abs(1.+dot_product(psi(theta,w,b),u)))

#The density of the transformed variational approximation:
def planar_flow(theta, u, w, b, mu, sigma):
	return np.exp(log_planar_flow(theta, u, w, b, mu, sigma))


#Initial values:
#See the Results section in the paper for how to replicate the figures there.
w = np.array([0.5,0.5])
u_arbitrary = np.array([-1.1,1.5])
b = -9.
mu = np.array([9.22,9.53])
sigma = np.array([3.85, 2.507])

#The transformation of u that ensures that the function f() is invertible:
u = u_arbitrary+((m(np.dot(w,u_arbitrary))-np.dot(w,u_arbitrary))/(np.linalg.norm(w)**2))*w

#Sampling from N(0,I) in two dimensions:
s = np.array([np.random.normal(0,1), np.random.normal(0,1)])

my_kappa = kappa(s,sigma,mu,w,b)
my_delta = delta(s,sigma,mu,my_kappa,u)
my_alpha = alpha(my_kappa)
my_beta = beta(w,s,my_alpha)
my_gamma = gamma(s,u,my_beta,my_delta)
my_rho = rho(u,my_beta,my_delta)
my_tau = tau(s,sigma,mu)
sum_squares = sum_my_sq(data)




########################################################################



#Gradient ascent for sigma only:

#Uncomment this chunk of code to run gradient descent:

'''
num_of_iterations = 200000
step_size_parameter = 0.00001
for i in range(num_of_iterations):
	current_grad = np.array([gradient_of_my_ELBO_wrt_sigma_1(s, sigma, mu, u, w, b, sum_squares,my_gamma,my_delta,my_rho,my_kappa,my_alpha), gradient_of_my_ELBO_wrt_sigma_2(s, sigma, mu, u, w, b, sum_squares,my_gamma,my_delta,my_rho,my_kappa,my_alpha)])

	sigma = sigma + step_size_parameter*current_grad
	if sigma[0]<0 or sigma[1]<0:
		print ("ERROR, SIGMA LESS THAN 0")
		sigma = sigma - step_size_parameter*current_grad
		break
	my_kappa = kappa(s,sigma,mu,w,b)
	my_delta = delta(s,sigma,mu,my_kappa,u)
	my_alpha = alpha(my_kappa)
	my_beta = beta(w,s,my_alpha)
	my_gamma = gamma(s,u,my_beta,my_delta)
	my_rho = rho(u,my_beta,my_delta)

	s = np.array([np.random.normal(0,1), np.random.normal(0,1)])

	if i%100 == 0:
		print (sigma, "Remaining iterations:", num_of_iterations-i)

print (sigma)
'''



########################################################################



#Gradient ascent for b only:

#Uncomment this chunk of code to run gradient descent:

'''
num_of_iterations = 400000
step_size_parameter = 0.0003
for i in range(num_of_iterations):
	current_grad = gradient_of_my_ELBO_wrt_b(s, sigma, mu, u, w, b, sum_squares,my_delta,my_rho,my_kappa,my_alpha)

	b = b + step_size_parameter*current_grad
	my_kappa = kappa(s,sigma,mu,w,b)
	my_delta = delta(s,sigma,mu,my_kappa,u)
	my_alpha = alpha(my_kappa)
	my_beta = beta(w,s,my_alpha)
	my_rho = rho(u,my_beta,my_delta)

	s = np.array([np.random.normal(0,1), np.random.normal(0,1)])

	if i%100 == 0:
		print (b, "Remaining iterations:", num_of_iterations-i)

print (b)
'''



########################################################################



#Gradient ascent for w only:

#Uncomment this chunk of code to run gradient descent:

'''
num_of_iterations = 160000
step_size_parameter = 0.00002
for i in range(num_of_iterations):
	current_grad = np.array([gradient_of_my_ELBO_wrt_w_1(s, sigma, mu, u, w, b, sum_squares,my_delta,my_kappa,my_alpha,my_tau,u_arbitrary), gradient_of_my_ELBO_wrt_w_2(s, sigma, mu, u, w, b, sum_squares,my_delta,my_kappa,my_alpha,my_tau,u_arbitrary)])

	w = w + step_size_parameter*current_grad
	u = u_arbitrary+((m(np.dot(w,u_arbitrary))-np.dot(w,u_arbitrary))/(np.linalg.norm(w)**2))*w
	my_kappa = kappa(s,sigma,mu,w,b)
	my_delta = delta(s,sigma,mu,my_kappa,u)
	my_alpha = alpha(my_kappa)
	my_beta = beta(w,s,my_alpha)
	my_rho = rho(u,my_beta,my_delta)
	my_tau = tau(s,sigma,mu)

	s = np.array([np.random.normal(0,1), np.random.normal(0,1)])

	if i%100 == 0:
		print (w, "Remaining iterations:", num_of_iterations-i)

print (w)
'''



########################################################################



#Gradient ascent for all parameters:

#Uncomment this chunk of code to run gradient descent:

'''
#ALL
num_of_iterations = 1000000
step_size_parameter_sigma = 0.00001
step_size_parameter_b = 0.00003
step_size_parameter_w = 0.000002
for i in range(num_of_iterations):

	current_grad_b = gradient_of_my_ELBO_wrt_b(s, sigma, mu, u, w, b, sum_squares,my_delta,my_rho,my_kappa,my_alpha)
	current_grad_sigma = np.array([gradient_of_my_ELBO_wrt_sigma_1(s, sigma, mu, u, w, b, sum_squares,my_gamma,my_delta,my_rho,my_kappa,my_alpha), gradient_of_my_ELBO_wrt_sigma_2(s, sigma, mu, u, w, b, sum_squares,my_gamma,my_delta,my_rho,my_kappa,my_alpha)])
	current_grad_w = np.array([gradient_of_my_ELBO_wrt_w_1(s, sigma, mu, u, w, b, sum_squares,my_delta,my_kappa,my_alpha,my_tau,u_arbitrary), gradient_of_my_ELBO_wrt_w_2(s, sigma, mu, u, w, b, sum_squares,my_delta,my_kappa,my_alpha,my_tau,u_arbitrary)])

	b = b + step_size_parameter_b*current_grad_b
	sigma = sigma + step_size_parameter_sigma*current_grad_sigma
	if sigma[0]<0 or sigma[1]<0:
		print ("ERROR, SIGMA LESS THAN 0")
		sigma = sigma - step_size_parameter_sigma*current_grad_sigma
		break
	w = w + step_size_parameter_w*current_grad_w
	u = u_arbitrary+((m(np.dot(w,u_arbitrary))-np.dot(w,u_arbitrary))/(np.linalg.norm(w)**2))*w
	my_kappa = kappa(s,sigma,mu,w,b)
	my_alpha = alpha(my_kappa)
	my_delta = delta(s,sigma,mu,my_kappa,u)
	my_beta = beta(w,s,my_alpha)
	my_rho = rho(u,my_beta,my_delta)
	my_gamma = gamma(s,u,my_beta,my_delta)
	my_tau = tau(s,sigma,mu)

	s = np.array([np.random.normal(0,1), np.random.normal(0,1)])

	if i%100 == 0:
		print (w, sigma, b, "Remaining iterations:", num_of_iterations-i)

print (w, sigma, b)
'''



#Defining the input space:
x = np.arange(0., 30, 0.3)
y = np.arange(0., 30, 0.3)
x, y = np.meshgrid(x, y)

#Applying the transformation to the input space:
transformed_meshgrid = [np.array(planar_transformation([x,y],u,w,b)[0]),np.array(planar_transformation([x,y],u,w,b)[1])]

#Plotting:
fig, ax = plt.subplots()

#This is the shape of the true posterior:
CS_x = ax.contour(x, y, get_unnormalized_density([x,y],data), zorder=1)

#This is the shape of the transformed variational approximation:
CS_y = ax.contour(transformed_meshgrid[0], transformed_meshgrid[1], planar_flow([x,y],u,w,b,mu,sigma), zorder=2)

#Uncomment to see the original variational approximation:
#CS_z = ax.contour(x, y, q_density([x,y],mu,sigma), zorder=3)

plt.show()
