from sklearn import linear_model, svm
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.linear_model import Ridge
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import datetime
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from sklearn.metrics import mean_squared_error, r2_score


years = range(2011, 2016)
files = ['CRNS0101-05-%d-CA_Yosemite_Village_12_W.txt' % y for y in years]
usecols = [3, 4, 8]
data = [np.loadtxt(f, usecols=usecols) for f in files]
data = np.vstack(data)
data[:, 1] = np.floor_divide(data[:, 1], 100) * 60 + np.mod(data[:, 1], 100)
valid = data[:, 2] > -1000
days = []
for i in data[valid, 0]:
	days.append(datetime.datetime.strptime(str(i), '%Y%m%d.0').timetuple().tm_yday)
my_data = zip(days,data[valid, 1])

x_train = my_data
y_train = data[valid, 2]


years1 = range(2016, 2017)
files1 = ['CRNS0101-05-%d-CA_Yosemite_Village_12_W.txt' % y for y in years1]
usecols1 = [3, 4, 8]
data1 = [np.loadtxt(f, usecols=usecols1) for f in files1]
data1 = np.vstack(data1)
data1[:, 1] = np.floor_divide(data1[:, 1], 100) * 60 + np.mod(data1[:, 1], 100)
valid1 = data1[:, 2] > -1000
days1 = []
for i in data1[valid1, 0]:
	days1.append(datetime.datetime.strptime(str(i), '%Y%m%d.0').timetuple().tm_yday)
my_data1 = zip(days1,data1[valid1, 1])

x_test = my_data1
y_test = data1[valid1, 2]

def rbf(days, minutes, sigma1, sigma2, centers1, centers2):
	x1 = np.array(rbf_kernel(np.array(days).reshape(-1,1), centers1, gamma=1.0/sigma1))
	x2 = np.array(rbf_kernel(np.array(minutes).reshape(-1,1), centers2, gamma=1.0/sigma2))
	return np.concatenate((x1, x2), axis=1)

def rbf_separate(days, minutes, sigma1, sigma2, centers1, centers2):
	x1 = np.array(rbf_kernel(np.array(days).reshape(-1,1), centers1, gamma=1.0/sigma1))
	x2 = np.array(rbf_kernel(np.array(minutes).reshape(-1,1), centers2, gamma=1.0/sigma2))
	return x1, x2

sigma1=750
sigma2=8000
centers1 = np.linspace(1, 365, 30).reshape(-1, 1)
centers2 = np.linspace(0, 1435, 35).reshape(-1, 1)
x_training = rbf(days[:-1], data[valid, 1][:-1], sigma1, sigma2, centers1, centers2)
x_testing = rbf(days1[:-1], data1[valid1, 1][:-1], sigma1, sigma2, centers1, centers2)

alpha=0.0001
regr = Ridge(alpha=alpha, fit_intercept=True)
regr.fit(x_training, y_train[:-1])
y_pred = regr.predict(x_testing)
print("Score on training data (both seasonal variations and daily variations) = ", regr.score(x_training, y_train[:-1]))
print("Score on testing data (both seasonal variations and daily variations) = ", regr.score(x_testing, y_test[:-1]))
print "MSE both seasonal variations and daily variations = ", mean_squared_error(y_test[:-1], y_pred)

all_minutes = np.linspace(0.0, 1435.0, 100)
all_days = np.linspace(0.0, 365.0, 100)


def fn(all_minutes_meshgrid, all_days_meshgrid, regr, centers1, centers2, sigma1, sigma2):
	expanded_all_days = np.array(rbf_kernel(all_days_meshgrid[:,0].reshape(-1, 1), centers1, gamma=1.0 / sigma1))
	expanded_all_minutes = np.array(rbf_kernel(all_minutes_meshgrid[0].reshape(-1, 1), centers2, gamma=1.0 / sigma2))
	expanded_all=[]
	for i in range(len(expanded_all_days)):
		for j in range(len(expanded_all_minutes)):
			expanded_all.append(np.hstack((expanded_all_days[i], expanded_all_minutes[j])))
	all_y = regr.predict(expanded_all)
	all_y = all_y.reshape(100,100)
	return all_y

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('Minute of the day')
ax.set_ylabel('Day of the year')
ax.set_zlabel('Temperature')
X = all_minutes
Y = all_days
X, Y = np.meshgrid(X, Y)
Z = fn(X, Y, regr, centers1, centers2, sigma1, sigma2)
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, label='Time-of-year contribution')
plt.show()


sigma1=750
sigma2=8000
centers1 = np.linspace(1, 365, 30).reshape(-1, 1)
centers2 = np.linspace(0, 1435, 35).reshape(-1, 1)
x_training = rbf_separate(days[:-1], data[valid, 1][:-1], sigma1, sigma2, centers1, centers2)
x_testing = rbf_separate(days1[:-1], data1[valid1, 1][:-1], sigma1, sigma2, centers1, centers2)


alpha=0.0001
regr = Ridge(alpha=alpha, fit_intercept=True)
regr.fit(x_training[1], y_train[:-1])
y_pred = regr.predict(x_testing[1])
print("Score on training data (daily variations) = ", regr.score(x_training[1], y_train[:-1]))
print("Score on testing data (daily variations) = ", regr.score(x_testing[1], y_test[:-1]))
print "MSE (daily variations) = ", mean_squared_error(y_test[:-1], y_pred)


all_minutes1 = np.array(rbf_kernel(all_minutes.reshape(-1, 1), centers2, gamma=1.0 / sigma2))
all_y_minutes = regr.predict(all_minutes1)
plt.plot(all_minutes, all_y_minutes, label='Time-of-day contribution')
plt.xlabel('Minute of the day')
plt.ylabel('Temperature')
plt.legend(loc='best')
plt.show()

alpha=0.0001
regr = Ridge(alpha=alpha, fit_intercept=True)
regr.fit(x_training[0], y_train[:-1])
y_pred = regr.predict(x_testing[0])
print("Score on training data (seasonal variations) = ", regr.score(x_training[0], y_train[:-1]))
print("Score on testing data (seasonal variations) = ", regr.score(x_testing[0], y_test[:-1]))
print "MSE (seasonal variations) = ", mean_squared_error(y_test[:-1], y_pred)

all_days1 = np.array(rbf_kernel(all_days.reshape(-1, 1), centers1, gamma=1.0 / sigma1))
all_y_days = regr.predict(all_days1)
plt.plot(all_days, all_y_days, label='Time-of-year contribution')
plt.xlabel('Day of the year')
plt.ylabel('Temperature')
plt.legend(loc='best')
plt.show()
