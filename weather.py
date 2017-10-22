from sklearn.linear_model import LogisticRegression
import numpy as np
import datetime
from itertools import compress

years = range(2011, 2016)
files = ['CRNS0101-05-%d-CA_Yosemite_Village_12_W.txt' % y for y in years]
usecols = [3, 9]
data = [np.loadtxt(f, usecols=usecols) for f in files]
data = np.vstack(data)
days = []
for i in range(len(data)):
	if i%288==0:
		days.append(datetime.datetime.strptime(str(data[:, 0][i]), '%Y%m%d.0').timetuple().tm_yday)
y_train=[]
summ=0
for i in range(len(data[:, 1])):
	summ+=data[:, 1][i]
	if i%288==287:
		y_train.append(summ)
		summ=0
valid=[]
my_data=zip(days, y_train)
for i in range(len(my_data)):
	valid.append(my_data[i][1] > -1000)
days_valid = list(compress(days, valid))
y_train_valid = list(compress(y_train, valid))
y=[]
for i in range(len(y_train_valid)):
	if y_train_valid[i]>0:
		y.append(1)
	else:
		y.append(0)
days_valid=np.array(days_valid).reshape(-1,1)


model = LogisticRegression(class_weight='balanced')
model = model.fit(days_valid, np.array(y))
for i in range(365):
	print "For day", i, "predicted value:", model.predict(i)


years1 = range(2016, 2017)
files1 = ['CRNS0101-05-%d-CA_Yosemite_Village_12_W.txt' % y for y in years1]
usecols1 = [3, 9]
data1 = [np.loadtxt(f, usecols=usecols1) for f in files1]
data1 = np.vstack(data1)
days1 = []
for i in range(len(data1)):
	if i%288==0:
		days1.append(datetime.datetime.strptime(str(data1[:, 0][i]), '%Y%m%d.0').timetuple().tm_yday)
y_test1=[]
summ1=0
for i in range(len(data1[:, 1])):
	summ1+=data1[:, 1][i]
	if i%288==287:
		y_test1.append(summ1)
		summ1=0
valid1=[]
my_data1=zip(days1, y_test1)
for i in range(len(my_data1)):
	valid1.append(my_data1[i][1] > -1000)
days_valid1 = list(compress(days1, valid1))
y_test_valid1 = list(compress(y_test1, valid1))
y1=[]
for i in range(len(y_test_valid1)):
	if y_test_valid1[i]>0:
		y1.append(1)
	else:
		y1.append(0)
days_valid1=np.array(days_valid1).reshape(-1,1)


print "Predicted values for the days in 2016:", model.predict(days_valid1)
print "Actual values for the days in 2016:", y1
correct=0
for i in range(len(y1)):
	if model.predict(days_valid1[i])==y1[i]:
		correct+=1
print "Accuracy:", float(correct)/float(len(y1))
