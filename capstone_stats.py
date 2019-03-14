import csv
import random
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
random.seed(324)

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

#Printing the participants:
#Format is: [age, gender, education level,
#time spent watching the treatment video,
#time spent watching the control video, Q1 answer,
#Q2 answer, time spent answering, self-assessment for difficulty,
#self-assessment for mental effort, self-assessment for how enjoyable]


print "---"
print participants[0]
print "---"
print participants[1]
print "---"
print participants[2]
print "---"
print participants[3]
print "---"
print participants[4]
print "---"
print participants[5]
print "---"
print participants[6]
print "---"
print participants[7]
print "---"
print participants[8]
print "---"
print participants[9]
print "---"

#Determining the group of the participant. Changes the format of participants to:
#[age, gender, education level,
#time spent watching the video, Q1 answer,
#Q2 answer, time spent answering, self-assessment for difficulty,
#self-assessment for mental effort, self-assessment for how enjoyable]
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

#printing the treatment-control assignments:
print treatment_control_assignment_list

#Changing the format of participants by adding the group assignment:
#[age, gender, education level,
#time spent watching the video, Q1 answer,
#Q2 answer, time spent answering, self-assessment for difficulty,
#self-assessment for mental effort, self-assessment for how enjoyable,
#group assignment]
for i in range(len(participants)):
	participants[i].append(treatment_control_assignment_list[i])

#Changing the format of participants by adding the score as a fraction out of 6:
#[age, gender, education level,
#time spent watching the video, Q1 answer,
#Q2 answer, time spent answering, self-assessment for difficulty,
#self-assessment for mental effort, self-assessment for how enjoyable,
#group assignment, score]
participants[0].append(0)
participants[1].append(0)
participants[2].append(0)
participants[3].append(0)
participants[4].append(1./6.)
participants[5].append(0.5)
participants[6].append(0)
participants[7].append(1./6.)
participants[8].append(1./6.)
participants[9].append(0)
participants[10].append(0)

#Printing various pairs of variables to observe important correlations:
group_scores = [[participants[i][-2],participants[i][-1]] for i in range(len(participants))]
print "group_scores", group_scores

age_scores = [[participants[i][0],participants[i][-1]] for i in range(len(participants))]
print "age_scores", age_scores

gender_scores = [[participants[i][1],participants[i][-1]] for i in range(len(participants))]
print "gender_scores", gender_scores

edLevel_scores = [[participants[i][2],participants[i][-1]] for i in range(len(participants))]
print "edLevel_scores", edLevel_scores

timeWatch_scores = [[participants[i][3],participants[i][-1]] for i in range(len(participants))]
print "timeWatch_scores", timeWatch_scores

timeAnswer_scores = [[participants[i][6],participants[i][-1]] for i in range(len(participants))]
print "timeAnswer_scores", timeAnswer_scores

difficulty_scores = [[participants[i][7],participants[i][-1]] for i in range(len(participants))]
print "difficulty_scores", difficulty_scores

mentalEffort_scores = [[participants[i][8],participants[i][-1]] for i in range(len(participants))]
print "mentalEffort_scores", mentalEffort_scores

enjoyable_scores = [[participants[i][9],participants[i][-1]] for i in range(len(participants))]
print "enjoyable_scores", enjoyable_scores


age_group = [[participants[i][0],participants[i][-2]] for i in range(len(participants))]
print "age_group", age_group

gender_group = [[participants[i][1],participants[i][-2]] for i in range(len(participants))]
print "gender_group", gender_group

edLevel_group = [[participants[i][2],participants[i][-2]] for i in range(len(participants))]
print "edLevel_group", edLevel_group

timeWatch_group = [[participants[i][3],participants[i][-2]] for i in range(len(participants))]
print "timeWatch_group", timeWatch_group

timeAnswer_group = [[participants[i][6],participants[i][-2]] for i in range(len(participants))]
print "timeAnswer_group", timeAnswer_group

difficulty_group = [[participants[i][7],participants[i][-2]] for i in range(len(participants))]
print "difficulty_group", difficulty_group

mentalEffort_group = [[participants[i][8],participants[i][-2]] for i in range(len(participants))]
print "mentalEffort_group", mentalEffort_group

enjoyable_group = [[participants[i][9],participants[i][-2]] for i in range(len(participants))]
print "enjoyable_group", enjoyable_group

#--------------------------------#
#Fisher's test:

null_hypothesis = -0.34 #(the average increase in the treatment group)

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
assignment_list = []
for j in range(11):
	if j in [2,4,5,8,10]:
		assignment_list.append(0)
	else:
		assignment_list.append(1)
control_average = calculate_avg_in_group_null(0,group_scores,null_hypothesis, assignment_list)
treatment_average = calculate_avg_in_group_null(1,group_scores,null_hypothesis, assignment_list)
observed_treatment_effect = treatment_average - control_average
print "Observed treatment effect =", observed_treatment_effect

#This part calculates the average treatment effect of all possible
#treatment-control assignments, assuming a sharp null hypothesis:
comb = list(combinations(range(11),5))
treatment_effects = []
for i in comb:
	assignment_list = []
	for j in range(11):
		if j in i:
			assignment_list.append(0)
		else:
			assignment_list.append(1)
	control_average = calculate_avg_in_group_null(0,group_scores,null_hypothesis, assignment_list)
	treatment_average = calculate_avg_in_group_null(1,group_scores,null_hypothesis, assignment_list)
	treatment_effects.append(treatment_average - control_average)

#Plotting a histogram of the average treatment effect of all possible
#treatment-control assignments, assuming a sharp null hypothesis:
plt.axvline(observed_treatment_effect, color='r', linewidth=1)
plt.hist(treatment_effects, bins=16)
plt.show()

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
print "left p =", float(count_smaller)/float(total)
print "right p =", float(count_larger)/float(total)
#If left p<0.025, then the number in the null hypothesis is unlikely to be that large.
#If right p<0.025, then the number in the null hypothesis is unlikely to be that small.

#--------------------------------#
#Bayesian approach:

num_simulations = 100000

#Posterior Dirichlet distribution:
control_dir = np.random.dirichlet([3,3,1,2,1,1,1],num_simulations)
treatment_dir = np.random.dirichlet([6,2,1,1,1,1,1],num_simulations)

#Calculating the differences in the sample averages of the two distributions:
differences = []
for i in range(len(control_dir)):
	difference = 0.
	for j in range(7):
		difference += (j/6.)*treatment_dir[i][j]
		difference -= (j/6.)*control_dir[i][j]
	differences.append(difference)

#Plotting a histogram of the differences:
plt.axvline(np.percentile(differences, 2.5), color='r', linewidth=1)
plt.axvline(np.percentile(differences, 97.5), color='r', linewidth=1)
plt.hist(differences, bins=100)
plt.show()

#Calculating the 95% credible interval:
print np.percentile(differences, 2.5)
print np.percentile(differences, 97.5)


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
