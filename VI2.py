import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from copy import deepcopy
np.random.seed(0)

real_data = [[360,50,12./18.],[810,60,14./24.],[275,130,29./35.],[170,250,15./15.],[770,280,20./32.],[95,285,25./33.],[540,320,10./14.],[40,350,8./16.],[430,400,14./16.],[940,405,22./24.],[90,410,13./24.],[950,490,18./18.],[500,500,21./25.],[50,550,24./28.],[970,600,17./25.],[770,680,12./21.],[715,730,35./39.],[175,770,18./33.],[770,815,16./27.]]

n_samples = 200
rng = np.random.RandomState(123)
cluster_centers = np.array([[-1, -1.5], [1, 1]])
cl_SDs = np.array([np.eye(2), np.array([[0.5,0.],[0.,0.5]])])
probability_of_cluster = np.array([0.5, 0.5])

cluster_assignments = np.array([rng.multinomial(1, probability_of_cluster) for _ in range(n_samples)]).T

samples_by_cluser_assignment = [cl_assignment[:, np.newaxis] * rng.multivariate_normal(cl_center, cl_SD, size=n_samples)
      for cl_assignment, cl_center, cl_SD in zip(cluster_assignments, cluster_centers, cl_SDs)]

all_samples = np.sum(np.dstack(samples_by_cluser_assignment), axis=2)

plt.figure(figsize=(5, 5))
plt.scatter(all_samples[:, 0], all_samples[:, 1], c='g', alpha=0.5)
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.scatter(cluster_centers[0, 0], cluster_centers[0, 1], c='r', s=100)
plt.scatter(cluster_centers[1, 0], cluster_centers[1, 1], c='b', s=100)

plt.show()


s=[]
for i in real_data:
	s.append(np.random.binomial(1, i[2], 1)[0])

get_data = []
for i in range(len(real_data)):
	if s[i]==1:
		get_data.append([real_data[i][0]/200.,real_data[i][1]/200.])

get_data = np.array(get_data)
print get_data

#plt.figure(figsize=(5, 5))
#plt.scatter(get_data[:, 0], get_data[:, 1], c='g', alpha=0.5)
#plt.xlim(0, 5)
#plt.ylim(0, 5)
#plt.show()

def a_2d_unit_gaussian(x, mu):
	return (1./(2*np.pi))*np.exp(-0.5*((x[0]-mu[0])**2+(x[1]-mu[1])**2))

def a_2d_half_gaussian(x, mu):
	return (1./np.pi)*np.exp(-((x[0]-mu[0])**2+(x[1]-mu[1])**2))

def gradient_of_2d_unit_gaussian(x,mu):
	return [-((mu[0]-x[0])*np.exp(-0.5*((x[0]-mu[0])**2+(x[1]-mu[1])**2)))/(2*np.pi),-((mu[1]-x[1])*np.exp(-0.5*((x[0]-mu[0])**2+(x[1]-mu[1])**2)))/(2*np.pi)]

def gradient_of_2d_half_gaussian(x,mu):
	return [-2*((mu[0]-x[0])*np.exp(-((x[0]-mu[0])**2+(x[1]-mu[1])**2)))/(np.pi),-2*((mu[1]-x[1])*np.exp(-((x[0]-mu[0])**2+(x[1]-mu[1])**2)))/(np.pi)]

def gradient_of_log_p_x_m(data, mu):
	mu = np.array(mu).reshape((2, 2))
	result = np.array([[0.,0.],[0.,0.]])
	for j in range(len(result)):
		for i in data:
			adder_0 = (gradient_of_2d_unit_gaussian(i,mu[0]))/(a_2d_unit_gaussian(i, mu[0])+a_2d_half_gaussian(i, mu[1]))
			result[0] += adder_0
			adder_1 = (gradient_of_2d_half_gaussian(i,mu[1]))/(a_2d_unit_gaussian(i, mu[0])+a_2d_half_gaussian(i, mu[1]))
			result[1] += adder_1
	return result

def evaluate_variational_posterior(location, mus, sigmas):
	rnorm = []
	for i in range(4):
		rnorm.append(norm.pdf(location[i],mus[i],sigmas[i]))
	return rnorm[0]*rnorm[1]*rnorm[2]*rnorm[3]

init_values_mu = np.array([-1., -1.5,  1., 1.])
init_values_omega = np.array([0., 0., 0., 0.])

def gradient_of_ELBO_wrt_mu(data, mu, w):
	exp_w = np.matrix(np.diag(w))
	sample = np.random.multivariate_normal(np.zeros(4), np.eye(4))
	theta = np.array(sample*exp_w)[0]+mu
	return gradient_of_log_p_x_m(data, theta).flatten()

def gradient_of_ELBO_wrt_omega(data, mu, w):
	exp_w = np.matrix(np.diag(w))
	sample = np.random.multivariate_normal(np.zeros(4), np.eye(4))
	theta = np.array(sample*exp_w)[0]+mu
	gradient_p = gradient_of_log_p_x_m(data, theta).flatten()
	multiplier = np.array(sample*exp_w)[0]
	return np.ones(4) + gradient_p*multiplier

def adaptive_step_size_GD(data, init_mu, init_omega, tau = 1., eta = [0.01, 0.1, 1., 10., 100.], alpha = 0.1, epsilon = 1e-16):
	eta_chosen = eta[1]
	i = 1
	rho = np.zeros(8)
	mu = init_mu
	w = init_omega
	g_gradient = gradient_of_ELBO(data, mu, w)
	s = np.zeros(8)
	s_old = [m**2 for m in g_gradient]
	while np.linalg.norm(g_gradient)>10:
		print "gradient:", np.linalg.norm(g_gradient)
		g_gradient = gradient_of_ELBO(data, mu, w)
		for k in range(8):
			s[k] = alpha*g_gradient[k]**2+(1-alpha)*s_old[k]
			rho[k] = eta_chosen*(i**(-0.5+epsilon))*(1./(tau+np.sqrt(s[k])))
			s_old[k]=s[k]
		for k in range(4):
			mu[k] += rho[k]*g_gradient[k]
		for k in range(4):
			w[k] += rho[4+k]*g_gradient[4+k]
		i += 1
	return mu, w

def fixed_step_size_GD(data, init_mu, init_omega):
	mu = init_mu
	w = init_omega
	g_gradient = gradient_of_ELBO(data, mu, w)
	while np.linalg.norm(g_gradient)>3.:
		print "gradient:", np.linalg.norm(g_gradient)
		g_gradient = gradient_of_ELBO(data, mu, w)
		for k in range(4):
			mu[k] += 0.00002*g_gradient[k]
		for k in range(4):
			w[k] += 0.00002*g_gradient[4+k]
	print mu,w
	return mu, w

def gradient_of_ELBO(data, mu, w):
	gr_mu = gradient_of_ELBO_wrt_mu(data, mu, w)
	gr_omega = gradient_of_ELBO_wrt_omega(data, mu, w)
	return np.concatenate((gr_mu, gr_omega))

mus, ws = adaptive_step_size_GD(all_samples, init_values_mu, init_values_omega)

sigmas = np.exp(ws)

print "Results:"
print "mu:", mus
print "sigma:", sigmas

print evaluate_variational_posterior(mus, mus, sigmas)
#plt.scatter(mus[0], mus[1], c='r', s=100)
#plt.scatter(mus[2], mus[3], c='b', s=100)
#plt.show()



def logp_normal_np(mu, tau, value):
    k = 2
    delta = lambda mu: value - mu
    return (-1 / 2.) * (k * np.log(2 * np.pi) + np.log(1./np.linalg.det(tau)) +
                         (delta(mu).dot(tau) * delta(mu)).sum(axis=1))

def threshold(zz):
    zz_ = deepcopy(zz)
    zz_[zz < np.max(zz) * 1e-2] = None
    return zz_

def plot_logp_normal(ax, mu, sd, cmap):
    f = lambda value: np.exp(logp_normal_np(mu, np.diag(1 / sd**2), value))
    g = lambda mu, sd: np.arange(mu - 3, mu + 3, .1)
    xx, yy = np.meshgrid(g(mu[0], sd[0]), g(mu[1], sd[1]))
    zz = f(np.vstack((xx.reshape(-1), yy.reshape(-1))).T).reshape(xx.shape)
    ax.contourf(xx, yy, threshold(zz), cmap=cmap, alpha=0.9)

fig, ax = plt.subplots(figsize=(5, 5))
plt.scatter(all_samples[:, 0], all_samples[:, 1], alpha=0.5, c='k')
plot_logp_normal(ax, np.array([mus[0],mus[1]]), np.array([1., 1.]), cmap='Reds')
plot_logp_normal(ax, np.array([mus[2],mus[3]]), np.array([0.5,0.5]), cmap='Blues')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.show()


