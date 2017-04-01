sequences=[]
sequences.append('TTCTACGGGGGGAGACCTTTACGAATCACACCGGTCTTCTTTGTTCTAGCCGCTCTTTTTCATCAGTTGCAGCTAGTGCATAATTGCTCACAAACGTATC')
sequences.append('TCTACGGGGGGCGTCATTACGGAATCCACACAGGTCGTTATGTTCATCTGTCTCTTTTCACAGTTGCGGCTTGTGCATAATGCTCACGAACGTATC')
sequences.append('TCTACGGGGGGCGTCTATTACGTCGCCAACAGGTCGTATGTTCATTGTCATCATTTTCATAGTTGCGGCCTGTGCGTGCTTACGAACGTATTCC')
sequences.append('TCCTAACGGGTAGTGTCATACGGAATCGACACGAGGTCGTATCTTCAATTGTCTCTTCACAGTTGCGGCTGTCCATAAACGCGTCCCGAACGTTATG')
sequences.append('TATCAGTAGGGCATACTTGTACGACATTCCCCGGATAGCCACTTTTTTCCTACCCGTCTCTTTTTCTGACCCGTTCCAGCTGATAAGTCTGATGACTC')
sequences.append('TAATCTATAGCATACTTTACGAACTACCCCGGTCCACGTTTTTCCTCGTCTTCTTTCGCTCGATAGCCATGGTAACTTCTACAAAGTTC')
sequences.append('TATCATAGGGCATACTTTTACGAACTCCCCGGTGCACTTTTTTCCTACCGCTCTTTTTCGACTCGTTGCAGCCATGATAACTGCTACAAACTTC')

def LCS(list1, list2, c):
	if c==[]:
		for i in range (len(list1)):
			a=[]
			for j in range(len(list2)):
				a.append(-1)
			c.append(a)
	if len(list1)==0 or len(list2)==0:
		return 0
	elif c[len(list1)-1][len(list2)-1]!=-1:
		return c[len(list1)-1][len(list2)-1]
	else:
		if list1[-1]==list2[-1]:
			result=LCS(list1[:-1],list2[:-1],c)
			c[len(list1)-1][len(list2)-1]=result+1
			return result+1
		else:
			result1=LCS(list1[:-1],list2,c)
			result2=LCS(list1,list2[:-1],c)
			c[len(list1)-1][len(list2)-1]=max(result1,result2)
			return max(result1,result2)

subs=[]
for i in range (0,6):
	for j in range (i+1,7):
		result=LCS(sequences[j],sequences[i],[])
		subs.append(result)
		print "The longest subsequence of", i, "and", j, "is", result, "."

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
print subs
print sorted(subs)
