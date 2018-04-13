# True data
places = ['At Home', 'Apollo', 'Dosa Hut', 'Shilparamam', 'Masjid', 'Anjaneya Temple', 'Spar']
M = 10000.    #large number
distances = [             #(in km)
    [M, 1., 0.85, 1.7, 0.7, 2., 1.3], #From At Home
    [1., M, 0.7, 2.0, 1.5, 1.9, 0.9], #From Apollo
    [0.85, 0.7, M, 1.3, 1.2, 2.4, 1.4], #From Dosa Hut
    [1.7, 2.0, 1.3, M, 2., 3.3, 2.7], #From Shilparamam
    [0.7, 1.5, 1.2, 2., M, 1.4, 1.1], #From Masjid
    [2., 1.9, 2.4, 3.3, 1.4, M, 1.], #From Anjaneya Temple
    [1.3, 0.9, 1.4, 2.7, 1.1, 1., M]  #From Spar
]
times = [[14*j for j in i] for i in distances]       #(in min)


#####################################################################################################


# Fake data
places = ['At Home', 'Apollo', 'Dosa Hut', 'Shilparamam', 'Masjid', 'Anjaneya Temple', 'Spar']
M = 10000.    #large number
distances = [             #(in km)
    [M, 0.3, 0.85, 1.7, 0.7, 2., 1.3], #From At Home
    [0.3, M, 0.7, 2.0, 1.5, 1.9, 0.9], #From Apollo
    [0.85, 0.7, M, 1.3, 1.2, 2.4, 1.4], #From Dosa Hut
    [1.7, 2.0, 1.3, M, 1., 1.3, 2.7], #From Shilparamam
    [0.7, 1.5, 1.2, 1., M, 1.4, 1.1], #From Masjid
    [2., 1.9, 2.4, 1.3, 1.4, M, 1.], #From Anjaneya Temple
    [1.3, 0.9, 1.4, 2.7, 1.1, 1., M]  #From Spar
]
times = [[14*j for j in i] for i in distances]       #(in min)


#####################################################################################################


from cvxpy import *
import numpy as np

#--- Variables
N = 7 # total number of sites
c = Bool(N*N) # choice matrix
obj = Minimize(np.ndarray.flatten(np.asarray(times))*c) # Minimize time

#Useful matrices:
indices_rows=[[1 if cell//N==row_number else 0 for cell in range(N*N)] for row_number in range(N)]
indices_columns=[[1 if cell%N==col_number else 0 for cell in range(N*N)] for col_number in range(N)]
transpose_matrix=[[1 if active_cell==cell//N+N*(cell%N) else 0 for cell in range(N*N)] for active_cell in range(N*N)]

#--- Constraints
con = [c.T*indices_rows[j]==1 for j in range(N)]    #The sum at each row should be 1
con.extend(c.T*indices_columns[i]==1 for i in range(N))    #The sum at each column should be 1
con.extend((transpose_matrix*c+c)[i]<=1 for i in range(N*N))    #We cannot have A-->B and B-->A

#We cannot have A-->B and B-->C and C-->A
con.extend(2*c.T*(np.identity(N*N)[N*i+j] + np.identity(N*N)[N*i+k] + np.identity(N*N)[N*j+i] + np.identity(N*N)[N*j+k] + np.identity(N*N)[N*k+i] + np.identity(N*N)[N*k+j]) <=5 for i in range(N-2) for j in range(i+1,N-1) for k in range(j+1,N))

# Form and solve problem.
prob = Problem(obj, con)
prob.solve()
print ("status:", prob.status)
c_true = np.reshape(np.array([0 if i<=0.5 else 1 for i in c.value]), (N, N)).T

def find_destination(places, bool_list):
    for bool_value in range(len(bool_list)):
        if bool_list[bool_value]==1:
            return places[bool_value]

for index in range(len(c_true)):
    print ("Traveling from", places[index], "to", find_destination(places, c_true[index]))
