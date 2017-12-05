import numpy as np
import matplotlib.pyplot as plt
import math
import random
random.seed(0)
np.random.seed(0)

maximums = []
for I in range(5,100):
	print "I=", I

	eta = 0.4
	memory=[]
	for i in range(200):
		memory.append(np.random.choice([-1.0, 1.0], size=(I,), p=[1./2, 1./2]))
	#print "memory[0]=", memory[0]
	#print "memory[1]=", memory[1]
	#print "etc..."

	max_n_mem=0
	for n_mem in range(1,200):
		#print "n_mem=", n_mem
		weight_matrix = np.array([[0.0 for j in range(I)] for i in range(I)])
		for n,i in enumerate(weight_matrix):
			for m,j in enumerate(i):
				if m!=n:
					for k in range(n_mem):
						weight_matrix[n][m]+=eta*(memory[k][n]*memory[k][m])
		#print "weight_matrix[0]=", weight_matrix[0]
		#print "weight_matrix[1]=", weight_matrix[1]
		#print "etc..."

		num_successes = 0
		for mem in range(n_mem):
			#print "mem=", mem
			corrupt = random.randint(0, I-2)
			#print "corrupt=", corrupt
			corrupted_memory = np.array([0.0 for i in range(I)])
			for i in range(I):
				if i!=corrupt:
					corrupted_memory[i]+=memory[mem][i]
				else:
					if memory[mem][i]==1.0:
						corrupted_memory[i]+=-1.0
					else:
						corrupted_memory[i]+=1.0
			#print "memory[mem]=", memory[mem]
			#print "corrupted_memory=", corrupted_memory
			current_memory = np.array([0.0 for i in range(I)])
			for i in range(I):
				if i!=corrupt:
					current_memory[i]+=memory[mem][i]
				else:
					if memory[mem][i]==1.0:
						current_memory[i]+=-1.0
					else:
						current_memory[i]+=1.0
			#print "current_memory=", current_memory
			new_memory = np.array([0.0 for i in range(I)])
			flag=False
			while (new_memory!=current_memory).all():
				if flag==True:
					for i in range(len(new_memory)):
						current_memory[i]=new_memory[i]
				if flag==False:
					new_memory = np.array([0.0 for i in range(I)])
					for i in range(I):
						if i!=corrupt:
							new_memory[i]+=memory[mem][i]
						else:
							if memory[mem][i]==1.0:
								new_memory[i]+=-1.0
							else:
								new_memory[i]+=1.0
					#print "init_new_memory=", new_memory
				for i in range(I):
					new_memory[i]=0.0
					for j in range(I):
						new_memory[i] += new_memory[j]*weight_matrix[i][j]
					if new_memory[i]>=0:
						new_memory[i] = 1.0
					else:
						new_memory[i] = -1.0
				flag=True
			#print "final_new_memory=", new_memory
			if (new_memory==memory[mem]).all():
				num_successes+=1
				#print "We got", new_memory, "=", memory[mem], "SUCCESS"
			#print "Now num_successes=", num_successes
		#print "final num_successes=", num_successes
		if num_successes==n_mem:
			#print "For I=",I,"works with n_mem=", n_mem
			#print "Setting max_n_mem=", n_mem
			max_n_mem=n_mem
		else:
			break
	#print "For I=",I,"the max is n_mem=", max_n_mem
	maximums.append(max_n_mem)

x=range(5,100)
y=np.convolve(maximums, [1.0/3.0, 1.0/3.0, 1.0/3.0])
plt.plot([i for i in range(5,100)], [0.138*i for i in range(5,100)])
plt.plot(x,y[1:len(y)-1])
plt.show()


