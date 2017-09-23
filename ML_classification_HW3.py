import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model, neighbors, metrics
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix
import pandas as pd

#DATASETS USED:
#TRAINING:
#df2.csv - contains the FIRST 999 entries in the LoanStats3d.csv file, which I took from the Lending Club Statisctics for approved loans in 2015.
#df3.csv - contains the FIRST 999 entries in the RejectStatsD.csv file, which I took from the Lending Club Statisctics for rejected loans in 2015.
#TESTING:
#df_long_test.csv - contains the LAST 999 entries in the LoanStats3d.csv file, which I took from the Lending Club Statisctics for approved loans in 2015.
#df_rej_test.csv - contains the LAST 999 entries in the RejectStatsD.csv file, which I took from the Lending Club Statisctics for rejected loans in 2015.

rej = pd.read_csv('df2.csv')
acc = pd.read_csv('df3.csv')

#I take only four columns into consideration - Amount Requested (in USD), Debt-To-Income Ratio (in %), Employment Length (in years), and a binary variable that indicates whether the loan was accepted or not.
accepted = acc[['loan_amnt', 'dti', 'emp_length']]
rejected = rej[['Amount Requested', 'Debt-To-Income Ratio', 'Employment Length']]
accepted.columns = ['Amount Requested', 'Debt-To-Income Ratio', 'Employment Length']

#One of the datasets includes a '%' sign that I had to remove because the two datasets should look identically prior to concatenating them.
rejected['Debt-To-Income Ratio']=[float(rejected['Debt-To-Income Ratio'][i][:-1]) for i in range(999)]
accepted['Debt-To-Income Ratio']=[float(rejected['Debt-To-Income Ratio'][i]) for i in range(999)]
#Manually adding the 'Accepted' binary variable.
accepted['Accepted'] = np.array([1 for i in range(999)])
rejected['Accepted'] = np.array([0 for i in range(999)])

#Same data processing as above but for the test set.
rej_test = pd.read_csv('df_rej_test.csv')
df_test = pd.read_csv('df_long_test.csv')
accepted_test = df_test[['loan_amnt', 'dti', 'emp_length']]
rejected_test = rej_test[['Amount Requested', 'Debt-To-Income Ratio', 'Employment Length']]
accepted_test.columns = ['Amount Requested', 'Debt-To-Income Ratio', 'Employment Length']
rejected_test['Debt-To-Income Ratio']=[float(rejected_test['Debt-To-Income Ratio'][i][:-1]) for i in range(999)]
accepted_test['Debt-To-Income Ratio']=[float(rejected_test['Debt-To-Income Ratio'][i]) for i in range(999)]
accepted_test['Accepted'] = np.array([1 for i in range(999)])
rejected_test['Accepted'] = np.array([0 for i in range(999)])

#Concatenating the accepted and rejected datasets into one.
frames = [accepted, rejected]
data_frame = pd.concat(frames).reset_index(drop=True)
frames2 = [accepted_test, rejected_test]
data_frame_test = pd.concat(frames2).reset_index(drop=True)

#Replacing the string for employment length with a numeric variable for the training set.
data_frame=data_frame.replace(to_replace='n/a', value=np.nan)
data_frame=data_frame.replace(to_replace='< 1 year', value=0.5)
data_frame=data_frame.replace(to_replace='1 year', value=1.0)
data_frame=data_frame.replace(to_replace='2 years', value=2.0)
data_frame=data_frame.replace(to_replace='3 years', value=3.0)
data_frame=data_frame.replace(to_replace='4 years', value=4.0)
data_frame=data_frame.replace(to_replace='5 years', value=5.0)
data_frame=data_frame.replace(to_replace='6 years', value=6.0)
data_frame=data_frame.replace(to_replace='7 years', value=7.0)
data_frame=data_frame.replace(to_replace='8 years', value=8.0)
data_frame=data_frame.replace(to_replace='9 years', value=9.0)
data_frame=data_frame.replace(to_replace='10+ years', value=10.0)

#Replacing the string for employment length with a numeric variable for the test set.
data_frame_test=data_frame_test.replace(to_replace='n/a', value=np.nan)
data_frame_test=data_frame_test.replace(to_replace='< 1 year', value=0.5)
data_frame_test=data_frame_test.replace(to_replace='1 year', value=1.0)
data_frame_test=data_frame_test.replace(to_replace='2 years', value=2.0)
data_frame_test=data_frame_test.replace(to_replace='3 years', value=3.0)
data_frame_test=data_frame_test.replace(to_replace='4 years', value=4.0)
data_frame_test=data_frame_test.replace(to_replace='5 years', value=5.0)
data_frame_test=data_frame_test.replace(to_replace='6 years', value=6.0)
data_frame_test=data_frame_test.replace(to_replace='7 years', value=7.0)
data_frame_test=data_frame_test.replace(to_replace='8 years', value=8.0)
data_frame_test=data_frame_test.replace(to_replace='9 years', value=9.0)
data_frame_test=data_frame_test.replace(to_replace='10+ years', value=10.0)

#Exclude the applicants with unknown employment length.
data_frame.dropna(axis=0, how='any', inplace=True)
data_frame_test.dropna(axis=0, how='any', inplace=True)

#I want to choose the optimal K for best results. I try values of K between 2 and 19.

K=[]
for i in range(2,20):
	K.append(i)

#I record the maximum accuracy that the model yields on the test set, as well as the optimal K that produces that maximum accuracy.
max_accuracy=0
optimal_K=3


for i in range(18):
	#I give the KNN classifier the three variables and the number of neighbors.
	data_for_classifier = zip(data_frame['Amount Requested'], data_frame['Debt-To-Income Ratio'], data_frame['Employment Length'])
	classifier = neighbors.KNeighborsClassifier(n_neighbors=K[i])
	#Classifier training:
	classifier.fit(data_frame, data_frame['Accepted'])

	#Test set - what we expect vs what the classifier predicts:
	expected = data_frame_test['Accepted']
	predicted = classifier.predict(data_frame_test)

	print "Model performance for K=", K[i]
	print("Classification report for classifier %s:\n%s\n"
	    % (classifier, metrics.classification_report(expected, predicted)))
	print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
	print("Accuracy:\n%s" % metrics.accuracy_score(expected, predicted))

	#Comparing the accuracy to the previous max accuracy and replacing if it is larger.
	if metrics.accuracy_score(expected, predicted)>max_accuracy:
		max_accuracy=metrics.accuracy_score(expected, predicted)
		optimal_K=K[i]

#After finding the optimal K, I train the model once again with that value of K:
data_for_classifier = zip(data_frame['Amount Requested'], data_frame['Debt-To-Income Ratio'], data_frame['Employment Length'])
classifier = neighbors.KNeighborsClassifier(n_neighbors=optimal_K)
classifier.fit(data_frame, data_frame['Accepted'])

#This is the model that predicts the largest loan amount that will be successfully funded for given individual.
#Details about the individual:
person_DTI_Ratio=30
person_Empl_Len=9

#Starting with a really low loan amount.
person_amount=100

#By default, the loan is not accepted.
person_accepted=0

#For a certain range of loan amounts, I predict whether the loan will be accepted. I return the largest loan amount that the classifier predicts will be accepted.
my_range=1500

#Creating the data frame with the different loan amounts. The formula is 100+50*i, for i ranging up to 1499. The max amount that the classifier classifies is thus about 75,000.
result = pd.DataFrame({'Amount Requested' : pd.Series([100+50*i for i in range(my_range)]),
	'Debt-To-Income Ratio' : pd.Series([person_DTI_Ratio for i in range(my_range)]),
	'Employment Length' : pd.Series([person_Empl_Len for i in range(my_range)]),
	'Accepted' : pd.Series([person_accepted for i in range(my_range)])})
cols=['Amount Requested', 'Debt-To-Income Ratio', 'Employment Length', 'Accepted']
result = result[cols]

#For each loan amount, the classifier returns 0 (rejected) or 1 (accepted) and I record the result in list_of_predictions.
list_of_predictions=[]
for i in range(my_range):
	expected = result['Accepted'][0+i:1+i]
	predicted = classifier.predict(result[0+i:1+i])
	list_of_predictions.append(1-metrics.confusion_matrix(expected, predicted)[0][0])

#I now find the maximum loan that the classifier predicts will be accepted.
max_loan=0
for i in range(my_range):
	if list_of_predictions[i]==1:
		max_loan=100+50*i

#Finally, I print the model performance on the test set once more.
print "Model performance:"
expected = data_frame_test['Accepted']
predicted = classifier.predict(data_frame_test)
print("Classification report for classifier %s:\n%s\n"
	% (classifier, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
print("Accuracy:\n%s" % metrics.accuracy_score(expected, predicted))

#FINAL RESULT:
print "RESULT:"
print "Max loan is", max_loan
