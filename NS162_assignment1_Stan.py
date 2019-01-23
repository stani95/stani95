import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('SandPConstantDollars.dat', skip_header=0, skip_footer=0, names=True, dtype=None, delimiter=' ')
nice_data = []
for i in data:
	nice_data.append([i[0],i[1]])
nice_data_tr = list(map(list, zip(*nice_data)))



def give_percentage_change_daily(my_data):
	to_return = []
	for i in range(len(my_data)-1):
		to_return.append([my_data[i+1][0],100*(my_data[i+1][1]-my_data[i][1])/my_data[i][1]])
	to_return_tr = list(map(list, zip(*to_return)))
	return to_return_tr

def give_percentage_change_weekly(my_data):
	to_return = []
	for i in range(len(my_data)-5):
		to_return.append([my_data[i+5][0],100*(my_data[i+5][1]-my_data[i][1])/my_data[i][1]])
	to_return_tr = list(map(list, zip(*to_return)))
	return to_return_tr

def give_percentage_change_monthly(my_data):
	to_return = []
	for i in range(len(my_data)-21):
		to_return.append([my_data[i+21][0],100*(my_data[i+21][1]-my_data[i][1])/my_data[i][1]])
	to_return_tr = list(map(list, zip(*to_return)))
	return to_return_tr

def give_percentage_change_yearly(my_data):
	to_return = []
	for i in range(len(my_data)-252):
		to_return.append([my_data[i+252][0],100*(my_data[i+252][1]-my_data[i][1])/my_data[i][1]])
	to_return_tr = list(map(list, zip(*to_return)))
	return to_return_tr

def give_percentage_change_custon(my_data, lag):
	to_return = []
	for i in range(len(my_data)-lag):
		to_return.append([my_data[i+lag][0],100*(my_data[i+lag][1]-my_data[i][1])/my_data[i][1]])
	to_return_tr = list(map(list, zip(*to_return)))
	return to_return_tr

def calculate_volatility(my_data):
	my_mean = np.mean(my_data)
	my_squared_deviations = []
	for i in my_data:
		my_squared_deviations.append((i-my_mean)**2)
	return np.sqrt(np.mean(my_squared_deviations))

def calculate_squared_volatility(my_data):
	my_mean = np.mean(my_data)
	my_squared_deviations = []
	for i in my_data:
		my_squared_deviations.append((i-my_mean)**2)
	return np.mean(my_squared_deviations)

daily_volatility = calculate_volatility(give_percentage_change_daily(nice_data)[1])
print ("Daily volatility:", daily_volatility)
weekly_volatility = calculate_volatility(give_percentage_change_weekly(nice_data)[1])
print ("Weekly volatility:", weekly_volatility)
monthly_volatility = calculate_volatility(give_percentage_change_monthly(nice_data)[1])
print ("Monthly volatility:", monthly_volatility)

volatilities_list = []
for i in range(1,101):
	volatilities_list.append(calculate_volatility(give_percentage_change_custon(nice_data,i)[1]))
squared_volatilities_list = []
for i in range(1,101):
	squared_volatilities_list.append(calculate_squared_volatility(give_percentage_change_custon(nice_data,i)[1]))


plt.plot(volatilities_list)
plt.xlabel('Lag')
plt.ylabel('Volatility')
plt.show()

plt.plot(squared_volatilities_list)
plt.xlabel('Lag')
plt.ylabel('Squared volatility')
plt.show()

def get_log(my_data):
	to_return = []
	for i in my_data:
		to_return.append(np.log(i))
	return to_return

def make_parabola(a,b,c,x):
	to_return = []
	for i in x:
		to_return.append(a*i*i+b*i+c)
	return to_return


plt.plot(nice_data_tr[0], nice_data_tr[1])
plt.xlabel('Time')
plt.ylabel('Stock price')
plt.show()

plt.hist(give_percentage_change_daily(nice_data)[1], bins=200)
plt.xlabel('Percentage change')
plt.ylabel('Frequency')
plt.show()

plt.plot(np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[1][:-1], np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[0])
plt.hist(give_percentage_change_weekly(nice_data)[1], bins=200)
plt.xlabel('Percentage change')
plt.ylabel('Frequency')
plt.show()

plt.hist(give_percentage_change_monthly(nice_data)[1], bins=200)
plt.xlabel('Percentage change')
plt.ylabel('Frequency')
plt.show()

plt.hist(give_percentage_change_yearly(nice_data)[1], bins=200)
plt.xlabel('Percentage change')
plt.ylabel('Frequency')
plt.show()

plt.plot(np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[1][:-1], get_log(np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[0]))
plt.xlabel('Percentage change')
plt.ylabel('Log frequency')
plt.xlim(-10,10)
plt.ylim(-1,7)
plt.show()

plt.plot(np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[1][:-1], get_log(np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[0]))
plt.plot(np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[1][:-1], make_parabola(-0.122,0.0274,5.291,np.histogram(give_percentage_change_weekly(nice_data)[1], bins=200)[1][:-1]))
plt.xlabel('Percentage change')
plt.ylabel('Log frequency')
plt.xlim(-10,10)
plt.ylim(-1,7)
plt.show()


