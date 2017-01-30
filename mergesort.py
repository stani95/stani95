from random import randint
from datetime import datetime
import matplotlib.pyplot as plt

#This is the implementation of insertion sort:
def insertion_sort(A):
	#The sublist A[0:i-1] is already sorted.
	for i in range (1,len(A)):
		j=i-1
		key=A[i]
		#We want to see where the key fits into the sorted sublist.
		while j>=0 and key<A[j]:
			#The key must go somewhere to the left of the j-th element in this case, so shifting one position.
			A[j+1]=A[j]
			j=j-1
		#Finally we have found the right place for the key and so we put it there.
		A[j+1]=key
	return A

#This function takes two sorted lists and merges them:
def merge(A,B):
	#The result of the merge is the list C.
	C=[]
	a=0
	b=0
	while a<len(A) and b<len(B):
		if A[a]>B[b]:
			#Append to C the smalles of the current two elements.
			C.append(B[b])
			#Change the current element of the corresponding list.
			b+=1
		else:
			#Append to C the smalles of the current two elements.
			C.append(A[a])
			#Change the current element of the corresponding list.
			a+=1
	if len(A)==a:
		#If one of the lists is already appended to C, append the rest of the other list.
		while b<len(B):
			C.append(B[b])
			b+=1
	if len(B)==b:
		#If one of the lists is already appended to C, append the rest of the other list.
		while a<len(A):
			C.append(A[a])
			a+=1
	return C

#This is the classic 2-way mergesort algorithm, implemented recursively:
def mergesort(A):
	if len(A)!=1:
		#Take the list, divide it into two, sort the two parts, and merge them together.
		A=merge(mergesort(A[0:len(A)/2]),mergesort(A[len(A)/2:len(A)]))
	#In the case of 1 element, it is a sorted list so return it.
	return A

#This function just returns the minimum of three numbers. It looks complicated because I've included how to handle inputs of "None".
#The second number it returns is 0 if a is the smallest, 1 if b is the smallest, 2 if c is the smallest.
def choosemin3(a,b,c):
	if a==None:
		if b==None:
			return c,2
		if c==None:
			return b,1
		if b>=c:
			return c,2
		else:
			return b,1
	if b==None:
		if a==None:
			return c,2
		if c==None:
			return a,0
		if a>=c:
			return c,2
		else:
			return a,0
	if c==None:
		if a==None:
			return b,1
		if b==None:
			return a,0
		if a>=b:
			return b,1
		else:
			return a,0
	if b>=a and c>=a:
		return a,0
	if b>=c and a>=c:
		return c,2
	if a>=b and c>=b:
		return b,1

#This function takes three sorted lists and merges them:
def merge3(A,B,C):
	#The result of the merge is the list D.
	D=[]
	a=0
	b=0
	c=0
	A.append(None)
	B.append(None)
	C.append(None)
	#I treat None as an infinitely large element. I append it so that no list goes out of bounds.
	while a!=len(A)-1 or b!=len(B)-1 or c!=len(C)-1:
		#Append the smallest of the current three numbers to D.
		D.append(choosemin3(A[a],B[b],C[c])[0])
		#Change the current element of the corresponding list.
		if choosemin3(A[a],B[b],C[c])[1]==0:
			a+=1
		elif choosemin3(A[a],B[b],C[c])[1]==1:
			b+=1
		elif choosemin3(A[a],B[b],C[c])[1]==2:
			c+=1
	#Remove the None element
	A.pop()
	B.pop()
	C.pop()
	return D

#This is the 3-way mergesort function:
def mergesort3(A):
	#The base case occurs when the length of A is eithe 1 or 2.
	if len(A)!=1 and len(A)!=2:
		#Take the list, divide it into three, sort the three parts, and merge them together.
		A=merge3(mergesort3(A[0:len(A)/3]),mergesort3(A[len(A)/3:2*len(A)/3]),mergesort3(A[2*len(A)/3:len(A)]))
	#In the case of 2 elements, just sort it manually.
	if len(A)==2:
		if A[0]<=A[1]:
			return A
		else:
			A[0]=A[0]+A[1]
			A[1]=A[0]-A[1]
			A[0]=A[0]-A[1]
			return A
	#In the case of 1 element, it is a sorted list so return it.
	return A

#This is the modified mergesort from (2):
def mergesort3_modified(A):
	#The number I chose is 25. Every list of less than 25 elements will be sorted by insertion sort.
	if len(A)<25:
		return insertion_sort(A)
	#In the case of a larger list, the mergesort procedure is applied.
	return merge3(mergesort3_modified(A[0:len(A)/3]),mergesort3_modified(A[len(A)/3:2*len(A)/3]),mergesort3_modified(A[2*len(A)/3:len(A)]))

#A sample unsorted list:
#A=[4,7,3,1,11,9,34,75,2,5,8,1,6,7,12,2,33,1,44]
#print mergesort3(A)
#print mergesort(A)
#print insertion_sort(A)
#print mergesort3_modified(A)

#This piece of code creates lists of length 100,101,102,...,999, tests the modified 3-way mergesort on them, and keeps the resulting times in lis_3m:
lis_3m=[]
for i in range (100,1000):
    lis=[]
    for j in range(0,i):
    	#The numbers in each list are randomly taken between -150 and 150.
        lis.append(randint(-150,150))
    startTime = datetime.now()
    mergesort3_modified(lis)
    curr=datetime.now() - startTime
    lis_3m.append(curr.microseconds)
    print "Test of modified 3-way mergesort number", i
plt.plot(lis_3m)

#This piece of code creates lists of length 100,101,102,...,999, tests the 3-way mergesort on them, and keeps the resulting times in lis_3:
lis_3=[]
for i in range (100,1000):
    lis=[]
    for j in range(0,i):
        lis.append(randint(-150,150))
    startTime = datetime.now()
    mergesort3(lis)
    curr=datetime.now() - startTime
    lis_3.append(curr.microseconds)
    print "Test of 3-way mergesort number", i
plt.plot(lis_3)

#This piece of code creates lists of length 100,101,102,...,999, tests the classic 2-way mergesort on them, and keeps the resulting times in lis_2:
lis_2=[]
for i in range (100,1000):
    lis=[]
    for j in range(0,i):
        lis.append(randint(-150,150))
    startTime = datetime.now()
    mergesort(lis)
    curr=datetime.now() - startTime
    lis_2.append(curr.microseconds)
    print "Test of classic 2-way mergesort number", i
plt.plot(lis_2)

#This is a table that takes 10 results from each list.
table=[[],[],[]]
table[0].append("lis_3")
table[1].append("lis3m")
table[2].append("lis_2")
for i in range (0,10):
	table[0].append(lis_3[i*len(lis_3)/10])
	table[1].append(lis_3m[i*len(lis_3m)/10])
	table[2].append(lis_2[i*len(lis_2)/10])

print table[0]
print table[1]
print table[2]

#The plot shows the running times of the three sorting algorithms.
#Red represents the classic 2-way mergesort, blue represents the modified 3-way mergesort, and green represents the 3-way mergesort.
plt.show()
