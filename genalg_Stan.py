sequences=[]
sequences.append('TTCTACGGGGGGAGACCTTTACGAATCACACCGGTCTTCTTTGTTCTAGCCGCTCTTTTTCATCAGTTGCAGCTAGTGCATAATTGCTCACAAACGTATC')
sequences.append('TCTACGGGGGGCGTCATTACGGAATCCACACAGGTCGTTATGTTCATCTGTCTCTTTTCACAGTTGCGGCTTGTGCATAATGCTCACGAACGTATC')
sequences.append('TCTACGGGGGGCGTCTATTACGTCGCCAACAGGTCGTATGTTCATTGTCATCATTTTCATAGTTGCGGCCTGTGCGTGCTTACGAACGTATTCC')
sequences.append('TCCTAACGGGTAGTGTCATACGGAATCGACACGAGGTCGTATCTTCAATTGTCTCTTCACAGTTGCGGCTGTCCATAAACGCGTCCCGAACGTTATG')
sequences.append('TATCAGTAGGGCATACTTGTACGACATTCCCCGGATAGCCACTTTTTTCCTACCCGTCTCTTTTTCTGACCCGTTCCAGCTGATAAGTCTGATGACTC')
sequences.append('TAATCTATAGCATACTTTACGAACTACCCCGGTCCACGTTTTTCCTCGTCTTCTTTCGCTCGATAGCCATGGTAACTTCTACAAAGTTC')
sequences.append('TATCATAGGGCATACTTTTACGAACTCCCCGGTGCACTTTTTTCCTACCGCTCTTTTTCGACTCGTTGCAGCCATGATAACTGCTACAAACTTC')

#Problem 1:
#Top-down approach.
def LCS(list1, list2, c):
	#Case 1: The first time I call the function, the array c is created, which keeps track of the solutions to all the subproblems.
	if c==[]:
		for i in range (len(list1)):
			a=[]
			for j in range(len(list2)):
				a.append(-1)
			c.append(a)
	#Case 2: One of the lists is empty.
	if len(list1)==0 or len(list2)==0:
		return 0
	#Case 3: The solution to the desired subproblem already exists in c, so we don't have to recompute it.
	elif c[len(list1)-1][len(list2)-1]!=-1:
		return c[len(list1)-1][len(list2)-1]
	#Case 4: The solution is not yet in c.
	else:
		#Subcase 1: The last letters are the same. In this case, remove the letters and increment the result.
		if list1[-1]==list2[-1]:
			result=LCS(list1[:-1],list2[:-1],c)
			#Once we have computed it, store it in c for later use.
			c[len(list1)-1][len(list2)-1]=result+1
			return result+1
		#Subcase 2: The last letters are different. In this case, compare the results when removing either last letter and choose the maximum.
		else:
			result1=LCS(list1[:-1],list2,c)
			result2=LCS(list1,list2[:-1],c)
			#Once we have found both results, store the larger one in c.
			c[len(list1)-1][len(list2)-1]=max(result1,result2)
			return max(result1,result2)

#Apply the algorithm to the given gene sequences.
subs=[]
for i in range (0,6):
	for j in range (i+1,7):
		result=LCS(sequences[j],sequences[i],[])
		subs.append(result)
		print "The longest subsequence of", i, "and", j, "is", result, "."

#Print the results in a nice table format.
subs=[]
for i in range (-1,7):
	if i!=6:
		print '\n',
		print i,
	for j in range (-1,7):
		if i==-1:
			if j!=6:
				print j+1, "  ",
		else:
			if j<i:
				print "    ",
			elif i==j:
				pass
			else:
				result=LCS(sequences[j],sequences[i],[])
				subs.append(result)
				print result, " ",

print "\n"

#Print the sorted list of lengths of common subsequences.
print sorted(subs)
