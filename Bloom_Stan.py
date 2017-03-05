import random
import string
import matplotlib.pyplot as plt
import mmh3
import math
from fnvhash import fnv1a_32
import numpy as np

#This function returns a random word with a certain length:
def randomword(length):
	return ''.join(random.choice(string.lowercase) for i in range(length))

#I keep the number of bits in the Bloom filter (m) constant.
numOfBits = 1450

#Reset the Bloom filter:
bloom = []
for i in range(numOfBits):
	bloom.append(0)

#Define the murmur hash function:
def murmur(elem):
	return mmh3.hash(elem)%numOfBits

#Define the fnv hash function:
def fnv(elem):
	return fnv1a_32(b'foo')%numOfBits

#Define my own hash function hash1:
def hash1(elem):
	total=0
	c=7
	d=3
	for i in elem:
		total+=((c**4)*ord(i)+d*ord(i)-ord(i)**2-c**3+2*d-c)%numOfBits
		c+=17
		d+=4
	total=total%numOfBits
	return total

#Bloom filter number 1:
#It uses only one hash function - murmur.

#This is how I add elements to the filter:
def add(elem, bloom):
	bloom[murmur(elem)]=1

#This is how I check if an element has been added:
def check(elem, bloom):
	return bool(bloom[murmur(elem)])

#The flag checks for false negatives to make sure the implementation is correct. It should always be False.
flag=False

#This is the list where I store the ratio of false positives over the number of elements checked.
listFalsePos=[]

#This is a list of the different values of the number of elements stored.
numList=[]

#The variable num tells us the number of items stored.
for num in range(2, 1000):
	numList.append(num)

	#Reset:
	bloom = []
	for i in range(numOfBits):
		bloom.append(0)
	falsePos=0
	words=[]
	words2=[]

	#Add random 15-letter words to the list words:
	for i in range(num):
		words.append(randomword(15))

	#Add random 15-letter words to the list words2:
	for i in range(num):
		words2.append(randomword(15))

	#Add each element of words to the Bloom filter:
	for i in words:
		add(i, bloom)

	#Check if these words were correctly added. Change the value of flag if something is wrong.
	for i in words:
		if check(i, bloom)==False:
			flag=True

	#Check if the elements of words2 have been added (they were not).
	#Each time the filter thinks that an item has been stored, increment the number of false positives.
	for i in words2:
		if check(i, bloom)==True and i not in words:
			falsePos+=1

	#Convert the total number of false positives to a ratio:
	listFalsePos.append(float(falsePos)/float(num))

	#Print:
	print "The result for", num, "is", 100*(float(falsePos)/float(num)), "%"

#Check that we didn't get false negatives:
if flag==True:
	print "ERROR!"
else:
	print "PERFECT!"

#Add the results to the plot:
plt.plot(numList, listFalsePos)


#Bloom filter number 2:
#It uses two hash function - murmur and fnv.

def add(elem, bloom):
	bloom[murmur(elem)]=1
	bloom[fnv(elem)]=1

def check(elem, bloom):
	return bool(bloom[murmur(elem)]) and bool(bloom[fnv(elem)])

flag=False
listFalsePos=[]
numList=[]

for num in range(2, 1000):
	numList.append(num)
	bloom = []
	for i in range(numOfBits):
		bloom.append(0)
	falsePos=0
	words=[]
	words2=[]
	for i in range(num):
		words.append(randomword(15))
	for i in range(num):
		words2.append(randomword(15))
	for i in words:
		add(i, bloom)
	for i in words:
		if check(i, bloom)==False:
			flag=True
	for i in words2:
		if check(i, bloom)==True and i not in words:
			falsePos+=1
	listFalsePos.append(float(falsePos)/float(num))
	print "The result for", num, "is", 100*(float(falsePos)/float(num)), "%"

if flag==True:
	print "ERROR!"
else:
	print "PERFECT!"

plt.plot(numList, listFalsePos)


#Bloom filter number 3:
#It uses three hash function - murmur, fnv and hash1.

def add(elem, bloom):
	bloom[murmur(elem)]=1
	bloom[fnv(elem)]=1
	bloom[hash1(elem)]=1

def check(elem, bloom):
	return bool(bloom[murmur(elem)]) and bool(bloom[fnv(elem)]) and bool(bloom[hash1(elem)])

flag=False
listFalsePos=[]
numList=[]

for num in range(2, 1000):
	numList.append(num)
	bloom = []
	for i in range(numOfBits):
		bloom.append(0)
	falsePos=0
	words=[]
	words2=[]
	for i in range(num):
		words.append(randomword(15))
	for i in range(num):
		words2.append(randomword(15))
	for i in words:
		add(i, bloom)
	for i in words:
		if check(i, bloom)==False:
			flag=True
	for i in words2:
		if check(i, bloom)==True and i not in words:
			falsePos+=1
	listFalsePos.append(float(falsePos)/float(num))
	print "The result for", num, "is", 100*(float(falsePos)/float(num)), "%"

if flag==True:
	print "ERROR!"
else:
	print "PERFECT!"

plt.plot(numList, listFalsePos)


#Make a duplicate of numList:
numList2=[]
for i in range(len(numList)):
	numList2.append(numList[i])

#The theoretically expected rate of false positives:
for i in range(len(numList)):
	numList[i]=math.exp(float(-numOfBits*(math.log(2))**2)/float(numList[i]))

#Add the expected rate to the plot:
plt.plot(numList2, numList)

#Show the plot
plt.show()
