import csv
import random
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
random.seed(324)
np.random.seed(184)

#A list of all the data for each of the participants:
participants = []

#A binary list of the treatment assignments of the subjects, where 0 is control and 1 is treatment.
treatment_control_assignment_list = []

#Getting the data from the messy .csv file from Qualtrics:
with open('real_data_table.csv', 'rb') as csv_table:
	csvreader = csv.reader(csv_table, delimiter='"')
	for k,row in enumerate(csvreader):
		if k>=20:
			for i,cell in enumerate(row):
				if i != 1 and i != 3:
					cell=cell.split(",")
				if i == 0:
					if cell[4] != '100':
						break
					participants.append([cell[18],cell[19],cell[20],cell[24],cell[28]])
				if i == 4:
					participants[-1].append(cell[3])
					participants[-1].append(cell[5])
					participants[-1].append(cell[6])
					participants[-1].append(cell[7])
				if i==1 or i==3:
					participants[-1].append(cell)

#Determining the group of the participant:
for i in participants:
	if i[4] == '' and i[3] != '':
		treatment_control_assignment_list.append(1)
		del i[4]
	elif i[3] == '' and i[4] != '':
		treatment_control_assignment_list.append(0)
		del i[3]
	else:
		print "ERROR"
		break

#Printing the treatment-control assignments:
#print "Treatment-control assignment list:", treatment_control_assignment_list

#Calculating the number of participants in the control group:
num_control = len([i for i in treatment_control_assignment_list if i==0])

#Adding the group assignment:
for i in range(len(participants)):
	participants[i].append(treatment_control_assignment_list[i])

#Adding the score as a fraction out of 6:
participants[0].append(0) #1
participants[1].append(0) #1
participants[2].append(0) #0
participants[3].append(0) #1
participants[4].append(1./6.) #0
participants[5].append(0.5) #0
participants[6].append(0) #1
participants[7].append(1./6.) #1
participants[8].append(1./6.) #0
participants[9].append(0) #1
participants[10].append(0) #0
participants[11].append(1./6) #0
participants[12].append(1./6.) #1
participants[13].append(0) #1
participants[14].append(0) #0
participants[15].append(0) #1

#Printing the participants' data:
#Format is: [age, gender, education level,
#time spent watching the video, Q1 answer,
#Q2 answer, time spent answering, self-assessment for difficulty,
#self-assessment for mental effort, self-assessment for how enjoyable,
#group assignment, score]

'''
for i in range(len(participants)):
	print i
	print participants[i]
	print "---"
'''

#Creating an array with the number of people in each score category
#for a specific experimental condition:
def array_results(group, participants):
	result = [0,0,0,0,0,0,0]
	for i in range(len(participants)):
		if participants[i][-2]==group:
			result[int(round(participants[i][-1]*6))]+=1
	return result

#Printing and visualizing various pairs of variables to observe important correlations:
group_scores = [[participants[i][-2],participants[i][-1]] for i in range(len(participants))]
#print "group_scores", group_scores

#plt.scatter(np.array(group_scores)[:,0],np.array(group_scores)[:,1])
#plt.xlabel('Group assignment')
#plt.ylabel('Test Score')
#plt.show()

age_scores = [[participants[i][0],participants[i][-1]] for i in range(len(participants))]
#print "age_scores", age_scores

#plt.scatter(np.array(age_scores)[:,0],np.array(age_scores)[:,1])
#plt.xlabel('Age')
#plt.ylabel('Test Score')
#plt.show()

gender_scores = [[participants[i][1],participants[i][-1]] for i in range(len(participants))]
#print "gender_scores", gender_scores

#plt.scatter(np.array(gender_scores)[:,0],np.array(gender_scores)[:,1])
#plt.xlabel('Gender')
#plt.ylabel('Test Score')
#plt.show()

edLevel_scores = [[participants[i][2],participants[i][-1]] for i in range(len(participants))]
#print "edLevel_scores", edLevel_scores

#plt.scatter(np.array(edLevel_scores)[:,0],np.array(edLevel_scores)[:,1])
#plt.xlabel('Education Level')
#plt.ylabel('Test Score')
#plt.show()
#print np.corrcoef(np.array(edLevel_scores)[:,0],np.array(edLevel_scores)[:,1])

timeWatch_scores = [[participants[i][3],participants[i][-1]] for i in range(len(participants))]
#print "timeWatch_scores", timeWatch_scores

#plt.scatter(np.array(timeWatch_scores)[:,0],np.array(timeWatch_scores)[:,1])
#plt.xlabel('Time spent watching the video')
#plt.ylabel('Test Score')
#plt.show()

timeAnswer_scores = [[participants[i][6],participants[i][-1]] for i in range(len(participants))]
#print "timeAnswer_scores", timeAnswer_scores

#plt.scatter(np.array(timeAnswer_scores)[:,0],np.array(timeAnswer_scores)[:,1])
#plt.xlabel('Time spent answering the questions')
#plt.ylabel('Test Score')
#plt.show()

difficulty_scores = [[participants[i][7],participants[i][-1]] for i in range(len(participants))]
#print "difficulty_scores", difficulty_scores

#plt.scatter(np.array(difficulty_scores)[:,0],np.array(difficulty_scores)[:,1])
#plt.xlabel('Perceived level of difficulty')
#plt.ylabel('Test Score')
#plt.show()

mentalEffort_scores = [[participants[i][8],participants[i][-1]] for i in range(len(participants))]
#print "mentalEffort_scores", mentalEffort_scores

#plt.scatter(np.array(mentalEffort_scores)[:,0],np.array(mentalEffort_scores)[:,1])
#plt.xlabel('Perceived level of mental effort')
#plt.ylabel('Test Score')
#plt.show()

enjoyable_scores = [[participants[i][9],participants[i][-1]] for i in range(len(participants))]
#print "enjoyable_scores", enjoyable_scores

#plt.scatter(np.array(enjoyable_scores)[:,0],np.array(enjoyable_scores)[:,1])
#plt.xlabel('Perceived level of enjoyment')
#plt.ylabel('Test Score')
#plt.show()

age_group = [[participants[i][0],participants[i][-2]] for i in range(len(participants))]
#print "age_group", age_group

#plt.scatter(np.array(age_group)[:,0],np.array(age_group)[:,1])
#plt.xlabel('Age')
#plt.ylabel('Group assignment')
#plt.show()

gender_group = [[participants[i][1],participants[i][-2]] for i in range(len(participants))]
#print "gender_group", gender_group

#plt.scatter(np.array(gender_group)[:,0],np.array(gender_group)[:,1])
#plt.xlabel('Gender')
#plt.ylabel('Group assignment')
#plt.show()

edLevel_group = [[participants[i][2],participants[i][-2]] for i in range(len(participants))]
#print "edLevel_group", edLevel_group

#plt.scatter(np.array(edLevel_group)[:,0],np.array(edLevel_group)[:,1])
#plt.xlabel('Education level')
#plt.ylabel('Group assignment')
#plt.show()

timeWatch_group = [[participants[i][3],participants[i][-2]] for i in range(len(participants))]
#print "timeWatch_group", timeWatch_group

#plt.scatter(np.array(timeWatch_group)[:,0],np.array(timeWatch_group)[:,1])
#plt.xlabel('Time spent watching the video')
#plt.ylabel('Group assignment')
#plt.show()

timeAnswer_group = [[participants[i][6],participants[i][-2]] for i in range(len(participants))]
#print "timeAnswer_group", timeAnswer_group

#plt.scatter(np.array(timeAnswer_group)[:,0],np.array(timeAnswer_group)[:,1])
#plt.xlabel('Time spent answering the questions')
#plt.ylabel('Group assignment')
#plt.show()

difficulty_group = [[participants[i][7],participants[i][-2]] for i in range(len(participants))]
#print "difficulty_group", difficulty_group

#plt.scatter(np.array(difficulty_group)[:,0],np.array(difficulty_group)[:,1])
#plt.xlabel('Perceived level of difficulty')
#plt.ylabel('Group assignment')
#plt.show()

mentalEffort_group = [[participants[i][8],participants[i][-2]] for i in range(len(participants))]
#print "mentalEffort_group", mentalEffort_group

#plt.scatter(np.array(mentalEffort_group)[:,0],np.array(mentalEffort_group)[:,1])
#plt.xlabel('Perceived level of mental effort')
#plt.ylabel('Group assignment')
#plt.show()

enjoyable_group = [[participants[i][9],participants[i][-2]] for i in range(len(participants))]
#print "enjoyable_group", enjoyable_group

#plt.scatter(np.array(enjoyable_group)[:,0],np.array(enjoyable_group)[:,1])
#plt.xlabel('Perceived level of enjoyment')
#plt.ylabel('Group assignment')
#plt.show()

#--------------------------------#
#Fisher's test:

null_hypothesis = 0. #(the average increase in the treatment group)
print "Fisher sharp null hypothesis:", null_hypothesis

#This function calculates the average potential outcomes for one of the
#two experimental groups, assuming a sharp null hypothesis:
def calculate_avg_in_group_null(group,data,null,new_assignment):
	if group == 0:
		my_sum = 0
		count = 0
		for i in range(len(data)):
			if new_assignment[i]==0:
				count += 1
				if data[i][0]==0:
					my_sum += data[i][1]
				else:
					my_sum += (data[i][1]-null)
		return float(my_sum)/float(count)
	if group == 1:
		my_sum = 0
		count = 0
		for i in range(len(data)):
			if new_assignment[i]==1:
				count += 1
				if data[i][0]==1:
					my_sum += data[i][1]
				else:
					my_sum += (data[i][1]+null)
		return float(my_sum)/float(count)

#This part calculates the average treatment effect of the observed
#treatment-control assignment, assuming a sharp null hypothesis:
control_average = calculate_avg_in_group_null(0,group_scores,null_hypothesis, treatment_control_assignment_list)
treatment_average = calculate_avg_in_group_null(1,group_scores,null_hypothesis, treatment_control_assignment_list)
observed_treatment_effect = treatment_average - control_average
print "Observed treatment effect =", observed_treatment_effect

#This part calculates the average treatment effect of all possible
#treatment-control assignments, assuming a sharp null hypothesis:
comb = list(combinations(range(len(participants)),num_control))
treatment_effects = []
for i in comb:
	assignment_list = []
	for j in range(len(participants)):
		if j in i:
			assignment_list.append(0)
		else:
			assignment_list.append(1)
	control_average = calculate_avg_in_group_null(0,group_scores,null_hypothesis, assignment_list)
	treatment_average = calculate_avg_in_group_null(1,group_scores,null_hypothesis, assignment_list)
	treatment_effects.append(treatment_average - control_average)

#Plotting a histogram of the average treatment effect of all possible
#treatment-control assignments, assuming a sharp null hypothesis:
#plt.axvline(observed_treatment_effect, color='r', linewidth=1)
#plt.hist(treatment_effects, bins=20)
#plt.show()

#Counting the number of average treatment effects more extreme than the
#observed one:
total = len(treatment_effects)
count_larger = 0
count_smaller = 0
for i in treatment_effects:
	if i<=observed_treatment_effect:
		count_smaller += 1
	if i>=observed_treatment_effect:
		count_larger += 1

#Printing the left-sided and right-sided p-value:
print "Left p-value =", float(count_smaller)/float(total)
print "Right p-value =", float(count_larger)/float(total)
#If left p<0.025, then the number in the null hypothesis is unlikely to be that large.
#If right p<0.025, then the number in the null hypothesis is unlikely to be that small.

#--------------------------------#
#Bayesian approach:

num_simulations = 50000

#Hyperparameter:
k = 0.4
print "Prior hyperparameter k =", k

#Prior Dirichlet distribution:
prior_dir_coeff = [k*i for i in [1.0,1.0,1.0,1.0,1.0,1.0,1.0]]
prior_control_dir = np.random.dirichlet(prior_dir_coeff,num_simulations)
prior_treatment_dir = np.random.dirichlet(prior_dir_coeff,num_simulations)

#Posterior Dirichlet distributions:
posterior_control_dir_coeff = np.add(np.array(prior_dir_coeff), np.array(array_results(0,participants)))
posterior_treatment_dir_coeff =  np.add(np.array(prior_dir_coeff), np.array(array_results(1,participants)))

posterior_control_dir = np.random.dirichlet(posterior_control_dir_coeff,num_simulations)
posterior_treatment_dir = np.random.dirichlet(posterior_treatment_dir_coeff,num_simulations)

#Sampling from the posterior:
scores = np.array([j/6. for j in range(7)])
differences = []
for i in range(len(posterior_control_dir)):
	sample_treatment = np.random.multinomial(len(participants)-num_control,posterior_treatment_dir[i])
	sample_control = np.random.multinomial(num_control,posterior_control_dir[i])
	differences.append(np.dot(scores,sample_treatment)/float(sum(sample_treatment))-np.dot(scores,sample_control)/float(sum(sample_control)))

#Plotting a histogram of the differences:
#plt.axvline(np.percentile(differences, 2.5), color='r', linewidth=1)
#plt.axvline(np.percentile(differences, 97.5), color='r', linewidth=1)
#plt.axvline(observed_treatment_effect, color='r', linewidth=1)
#plt.hist(differences, bins=100)
#plt.show()

#Calculating the 95% credible interval:
print "95% credible interval: [", np.percentile(differences, 2.5), ",", np.percentile(differences, 97.5),"]"

#Calculate probabilities:
probability_of_less_than = 0
for i in np.linspace(2.5,97.5,(97.5-2.5)/0.5+1):
	if np.percentile(differences, i)<probability_of_less_than:
		continue
	else:
		print "The probability of obtaining less than", probability_of_less_than, "ATE is approximately:", i, "percent."
	break

#Sampling from prior:
scores = np.array([j/6. for j in range(7)])
differences = []
tr_max = []
co_max = []
for i in range(len(prior_control_dir)):
	sample_treatment = np.random.multinomial(len(participants)-num_control,prior_treatment_dir[i])
	sample_control = np.random.multinomial(num_control,prior_control_dir[i])
	differences.append(np.dot(scores,sample_treatment)/float(sum(sample_treatment))-np.dot(scores,sample_control)/float(sum(sample_control)))
	tr_max.append(max(sample_treatment))
	co_max.append(max(sample_control))

#Plotting a histogram of the differences (prior):
#plt.axvline(np.percentile(differences, 2.5), color='r', linewidth=1)
#plt.axvline(np.percentile(differences, 97.5), color='r', linewidth=1)
#plt.axvline(observed_treatment_effect, color='r', linewidth=1)
#plt.hist(differences, bins=100)
#plt.show()

#Treatment:
#Plotting the distribution of the max number of people who scored the same number of points:
#plt.axvline(7, color='r', linewidth=1)
#plt.hist(tr_max, bins=10)
#plt.show()

#Calculating the number of simulations for which the max number of people
#in the treatment group who scored the same number of points is less than
#or equal to the observed value (7)
count_tr_eq = 0
count_tr_neq = 0
for i in tr_max:
	if i<=7:
		count_tr_eq += 1
	if i<7:
		count_tr_neq += 1
#print "Number of simulations for which the max number of people in the treatment group who scored the same number of points is less than or equal to 7:", count_tr_eq
#print "Number of simulations for which the max number of people in the treatment group who scored the same number of points is strictly less than 7:", count_tr_neq

#Control:
#Plotting the distribution of the max number of people who scored the same number of points:
#plt.axvline(3, color='r', linewidth=1)
#plt.hist(co_max, bins=10)
#plt.show()

#Calculating the number of simulations for which the max number of people
#in the control group who scored the same number of points is less than
#or equal to the observed value (3)
count_co_eq = 0
count_co_neq = 0
for i in co_max:
	if i<=3:
		count_co_eq += 1
	if i<3:
		count_co_neq += 1
#print "Number of simulations for which the max number of people in the control group who scored the same number of points is less than or equal to 3:", count_co_eq
#print "Number of simulations for which the max number of people in the control group who scored the same number of points is strictly less than 3:", count_co_neq

#Calculating the 95% credible interval (prior):
#print "95% credible interval (prior): [", np.percentile(differences, 2.5), ",", np.percentile(differences, 97.5),"]"


#---------------------------#
#T-Test
from scipy.stats import t

control_average = calculate_avg_in_group_null(0,group_scores,null_hypothesis, treatment_control_assignment_list)
treatment_average = calculate_avg_in_group_null(1,group_scores,null_hypothesis, treatment_control_assignment_list)
observed_treatment_effect = treatment_average - control_average

control_group_scores = []
treatment_group_scores = []
for i in range(len(participants)):
	if participants[i][-2]==0:
		control_group_scores.append(participants[i][-1])
	else:
		treatment_group_scores.append(participants[i][-1])

len_treatment = len(treatment_group_scores)
len_control = len(control_group_scores)
min_sample_size = min(len_control, len_treatment)

std_treatment = np.std(treatment_group_scores)
std_control = np.std(control_group_scores)

print "Average score in the treatment group:", treatment_average
print "Average score in the control group:", control_average
print "Standard deviation of the treatment group:", std_treatment
print "Standard deviation of the control group:", std_control

standard_error = np.sqrt((std_treatment**2/len_treatment)+((std_control**2)/len_control))
t_statistic = observed_treatment_effect/standard_error

#p-value:
print "p-value =", t.cdf(t_statistic, min_sample_size-1)

#Confidence interval:
print "Confidence interval: [", observed_treatment_effect + standard_error*t.ppf(0.025, min_sample_size-1), ",", observed_treatment_effect + standard_error*t.ppf(0.975, min_sample_size-1),"]"

#Significance level:
alpha = 0.025

hypothesis = 0.24 #--> needed for power of 0.85

print "Power of a test with", min_sample_size, "participants in the smaller group, where the alternative hypothesis is an improvement of", hypothesis, ":", t.cdf(hypothesis/standard_error-t.ppf(1-alpha, min_sample_size-1),min_sample_size-1)

pooled_SD = np.sqrt((((std_control*np.sqrt(len(control_group_scores))/np.sqrt(len(control_group_scores)-1))**2)*(len_control-1)+((std_treatment*np.sqrt(len(treatment_group_scores))/np.sqrt(len(treatment_group_scores)-1))**2)*(len_treatment-1))/(len_control+len_treatment-2))
print "For this alternative hypothesis, Cohen's d=", hypothesis/pooled_SD, "which is very large. To capture smaller effect sizes, I need a larger sample size."

print "Observed effect Cohen's d=", observed_treatment_effect/pooled_SD, "which is considered large."








#I used this code to shuffle the respondents' answers before the grading,
#in order to not bias myself.
'''
random.shuffle(participants)
#print "Reshuffled list participants : ",  participants

for i in range(len(participants)):
	print "Participant number", i+1,":"
	print "-----------------"
	print participants[i][4], "\n\n", participants[i][5]
	print "-----------------", "\n"
	print participants[i]
	print "-----------------", "\n"
'''

