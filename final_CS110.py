import math

#This function takes a sorted list (largest to smallest) and a number as inputs.
#It returns the index of the number in the list, if we were to insert it there.
def binary_search(search_list, search_value):
	l=len(search_list)
	#This is a binary search.
	#I compare the search_value to the number standing at the middle of the list and I go left or right depending on the result.
	#I stop recursing when the length of the list becomes 1.
	if l==1:
		if search_list[0]<search_value:
			return 0
		else:
			return 1
	else:
		if search_value>search_list[l/2]:
			return binary_search(search_list[0:l/2], search_value)
		else:
			return l/2+binary_search(search_list[l/2:l], search_value)

#This function builds the canonical intervals from my_list.
def create_canonicals(my_list):
	#temp_canonical contains all canonical intervals.
	#The order of insertion ensures that the following (heap-like) property holds:
	#Take the canonical interval at position i. If we split it into two, we get two more canonical intervals.
	#These canonical intervals are at positions 2i+1 and 2i+2.
	#We can represent temp_canonical as a tree. In this case, the children of a node at position i are at positions 2i+1 and 2i+2.
	temp_canonical=[]
	for i in range(0,int(math.log(len(my_list),2))+1):
		#For each level of the tree (we have log(n) levels):
		for j in range(0, 2**i):
			#Append the corresponding intervals. The deeper the level, the thinner the cuts.
			length=len(my_list)/(2**i)
			temp_canonical.append(my_list[j*length:(j+1)*length])
	return temp_canonical

#This is the preprocessing function. We apply it once to the list and then we can perform as many queries as we want with at most 1 comparison each.
def RMQ_Preprocess(my_list):
	canonicals=create_canonicals(my_list)

	#leftMins is not computed here, just initialized. I initialize it as having the same dimentions as canonicals, but having a None value everywhere.
	leftMins=[]
	count=-1
	for i in canonicals:
		count+=1
		leftMins.append([])
		for j in i:
			leftMins[count].append(None)

	#The same applies to rightMins.
	rightMins=[]
	count=-1
	for i in canonicals:
		count+=1
		rightMins.append([])
		for j in i:
			rightMins[count].append(None)

	#This is where leftMins and rightMins are computed:
	leftMins=create_leftMins(canonicals, leftMins, 0)
	rightMins=create_rightMins(canonicals, rightMins, 0)

	return canonicals, leftMins, rightMins

#How to create leftMins:
def create_leftMins(canonicals, leftMins, position):
	#position indicates the index of the canonical interval that I wish to transform into a leftMin list.

	if len(leftMins[position])==1:
		#If the length of the canonical list (canonicals and leftMins have the same dimentions) is one, I just take it.
		leftMins[position][0]=canonicals[position][0]
		return leftMins[position][0]

	else:
		#Else, I check if I have computed the children of the current interval. If not, I should compute them first.
		if None in leftMins[2*position+1]:
			create_leftMins(canonicals, leftMins, 2*position+1)
		if None in leftMins[2*position+2]:
			create_leftMins(canonicals, leftMins, 2*position+2)

		#Once I have the children, I use them to build the parent.
		for i in range(0,len(leftMins[position])/2):
			#The first half of the interval is the same as the first child.
			leftMins[position][i]=leftMins[2*position+1][i]

		#To compute the second half, I must see where the min of the first half stands within the values in the second child.
		first_half_min=leftMins[2*position+1][-1]
		position_of_first_half_min=binary_search(leftMins[2*position+2],first_half_min)

		#I compute the values in the second half one by one,
		#depending on whether the corresponding value in the second child is larger or smaller than the min of the first half. 
		for i in range(0,len(leftMins[position])/2):
			if position_of_first_half_min>i:
				leftMins[position][i+len(leftMins[position])/2]=first_half_min
			else:
				leftMins[position][i+len(leftMins[position])/2]=leftMins[2*position+2][i]

	return leftMins

#How to create rightMins:
#The process is analogous to the process for leftMins.
def create_rightMins(canonicals, rightMins, position):

	if len(rightMins[position])==1:
		rightMins[position][0]=canonicals[position][0]
		return rightMins[position][0]

	else:
		if None in rightMins[2*position+1]:
			create_rightMins(canonicals, rightMins, 2*position+1)
		if None in rightMins[2*position+2]:
			create_rightMins(canonicals, rightMins, 2*position+2)

		for i in range(0,len(rightMins[position])/2):
			rightMins[position][i]=rightMins[2*position+2][i]

		second_half_min=rightMins[2*position+2][-1]
		position_of_second_half_min=binary_search(rightMins[2*position+1],second_half_min)

		for i in range(0,len(rightMins[position])/2):
			if position_of_second_half_min>i:
				rightMins[position][i+len(rightMins[position])/2]=second_half_min
			else:
				rightMins[position][i+len(rightMins[position])/2]=rightMins[2*position+1][i]

	return rightMins

#This is the Query function. It uses canonicals, leftMins, and rightMins, which were computed during preprocessing.
def RMQ_Queries(canonicals, current_canonical, leftMins, rightMins, index1, index2):

	#The trivial case an interval of length 1.
	if len(canonicals[current_canonical])==1:
		return canonicals[current_canonical][0]

	#The case where the lower bound of the subset coincides with the lower bound of the current canonical interval.
	if index1==0:
		return leftMins[current_canonical][index2 - index1]

	#The case where the upper bound of the subset coincides with the upper bound of the current canonical interval.
	if index2==len(canonicals[current_canonical])-1:
		return rightMins[current_canonical][index2 - index1]

	#If none of the previous cases applies, we use the children to get the desired minimum.
	current_canonical=2*current_canonical+1

	#If the subset is contained in the left child, call the same function for that child.
	if index2<=len(canonicals[current_canonical])-1:
		return RMQ_Queries(canonicals, current_canonical, leftMins, rightMins, index1, index2)

	#If the subset is contained in the right child, call the same function for that child.
	elif index1>=len(canonicals[current_canonical]):
		index1-=len(canonicals[current_canonical])
		index2-=len(canonicals[current_canonical])
		return RMQ_Queries(canonicals, current_canonical+1, leftMins, rightMins, index1, index2)

	#If neither of these applies, then the lower bound of the subset is in the left child and the upper bound is in the right child.
	#We use just one comparison to finally get the result.
	else:
		return min(rightMins[current_canonical][len(canonicals[current_canonical])-1-index1], leftMins[current_canonical+1][index2-len(canonicals[current_canonical])])


#A list of 8 elements.
my_list=[6,3,4,7,1,2,5,8]

#Preprocessing.
canonicals, leftMins, rightMins = RMQ_Preprocess(my_list)

#Performing queries and printing the results.
print "The list is", my_list
for i in range(0,8):
	for j in range(i,8):
		print "For indeces=", i, j, ",the sublist=", my_list[i:j+1], "and the min element in the sublist is", RMQ_Queries(canonicals, 0, leftMins, rightMins, i, j)
