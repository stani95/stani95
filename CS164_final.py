import cvxpy as cvx
import numpy as np

# Input constraints
max_inp = 0.4

N = 12 # Steps

precision=1 # Precision

# Defining the target state
targetLHS = np.matrix([[-1, 0],[0, -1],[1, 0],[0, 1]])
targetRHS = np.matrix([-4.,-7.,5.,8.]).T

#Defining the boundary
boundaryLHS = targetLHS
boundaryRHS = np.matrix([0.5,0.5,5.,8.]).T

# Defining the obstacle
obsLHS = targetLHS

#coord_of_obst_list=[[0.5,0.5,1.5,3.], [2.5,-0.5,3.5,3.], [-0.5,4.,1.5,6.5], [3.4,6.4,3.5,6.5]]
coord_of_obst_list=[[0.5,0.5,1.5,3.],[2.5,-0.5,3.5,3.],[-0.5,4.,1.5,6.5]]
#coord_of_obst_list=[[0.5,0.5,1.5,3.],[2.5,-0.5,3.5,3.]]
#coord_of_obst_list=[[0.5,0.5,1.5,3.]]
num_obst = len(coord_of_obst_list)
obsRHS_list=[]
for i in range(num_obst):
    obsRHS_list.append( np.array([[-coord_of_obst_list[i][0]], [-coord_of_obst_list[i][1]], [coord_of_obst_list[i][2]], [coord_of_obst_list[i][3]]]) )

# Vertices of the obstacle
obsVerts=[]
for i in range(num_obst):
    obsVerts.append(np.asarray([[coord_of_obst_list[i][0], coord_of_obst_list[i][0], coord_of_obst_list[i][2], coord_of_obst_list[i][2], coord_of_obst_list[i][0]], [coord_of_obst_list[i][1], coord_of_obst_list[i][3], coord_of_obst_list[i][3], coord_of_obst_list[i][1], coord_of_obst_list[i][1]]]))

# Defining the system matrices
A = np.matrix('1,0,1,0;0,1,0,1;0,0,1,0;,0,0,0,1')
B = np.matrix('0.5,0;0,0.5;1,0;0,1')

#Defining the buffer
buffer = np.matrix('1;1;1;1')
buffer = buffer/(precision*2*np.sqrt(2))

# Defining the decision variables
X = cvx.Variable(4,N+1)
U = cvx.Variable(2,N)

#Defining the Boolean slack variables
b_p = cvx.Bool(4*num_obst,(precision-1)*(N))
b_p1 = cvx.Bool(4*num_obst,N)
b_p2 = cvx.Bool(4*num_obst,N)
b_qq = cvx.Bool(3)

# Big-M
M = 2000

# Define dynamic constraints

## Initial condition
con = [X[:,0] == np.matrix('0;0;0;0')]
## Dynamics
con.extend([X[:,i+1] == A*X[:,i] + B*U[:,i] for i in range(N)])
## Input constraints
con.extend([cvx.norm(U[:,i],np.inf) <= max_inp for i in range(N)])
## Obstacle avoidance
for obstacle in range(num_obst):
    for k in range(precision):
        weight1=(k)/precision
        weight2=1-(k)/precision
        if k==0:
            #For the state positions
            weight1=1
            weight2=0
            con.extend([obsLHS * (weight1*X[0:2,i]+weight2*X[0:2,i+1]) >= obsRHS_list[obstacle] + buffer*cvx.norm(X[0:2,i+1]-X[0:2,i]) - M*b_p1[4*obstacle:4*(obstacle+1),i] for i in range(1,N)])
            con.extend([obsLHS * (weight1*X[0:2,i]+weight2*X[0:2,i+1]) >= obsRHS_list[obstacle] + buffer*cvx.norm(X[0:2,i]-X[0:2,i-1]) - M*b_p2[4*obstacle:4*(obstacle+1),i] for i in range(1,N)])
            #Initial state
            con.extend([obsLHS * (weight1*X[0:2,0]+weight2*X[0:2,0+1]) >= obsRHS_list[obstacle] + buffer*cvx.norm(X[0:2,0+1]-X[0:2,0]) - M*b_p1[4*obstacle:4*(obstacle+1),0] ])
            #Final state
            con.extend([obsLHS * (weight1*X[0:2,N]+weight2*X[0:2,N-1]) >= obsRHS_list[obstacle] + buffer*cvx.norm(X[0:2,N]-X[0:2,N-1]) - M*b_p2[4*obstacle:4*(obstacle+1),0] ])
        else:
            #For the division (in-between) points:
            con.extend([obsLHS * (weight1*X[0:2,i]+weight2*X[0:2,i+1]) >= obsRHS_list[obstacle] + buffer*cvx.norm(X[0:2,i+1]-X[0:2,i]) - M*b_p[4*obstacle:4*(obstacle+1),(k-1)*(N)+i] for i in range(0,N)])
    #Putting constraints on the Boolean slack variables
    con.extend([sum(b_p[4*obstacle:4*(obstacle+1),i]) <= 3 for i in range((precision-1)*(N)) ])
    con.extend([sum(b_p1[4*obstacle:4*(obstacle+1),i]) <= 3 for i in range(N) ])
    con.extend([sum(b_p2[4*obstacle:4*(obstacle+1),i]) <= 3 for i in range(N) ])

## Terminal constraints allowing less than N steps:
#con.extend([targetLHS * X[0:2,i+1] <= targetRHS + M*np.matrix('1;1;1;1')*(1-b_qq[i]) for i in range(N)])
#con.extend([sum(b_qq) >= 1])

# Terminal constraint on the N-th step:
con.extend([targetLHS * X[0:2,N] <= targetRHS])

## Boundary constraints
con.extend([boundaryLHS * X[0:2,i+1] <= boundaryRHS for i in range(N)])

# Defining the objective
obj = cvx.Minimize(sum([cvx.norm(U[:,i],1) for i in range(0,N)]))

# Solving the optimization problem
print ("N=",N)
print ("Maximum input=",max_inp)
print ("precision=", precision)
prob = cvx.Problem(obj, con)
prob.solve()
print ("status:", prob.status)

##################################################################################

#Plotting
import matplotlib.pyplot as plt
x_vals = X.value.T
u_vals = U.value.T

plt.figure()
plt.plot(x_vals[:,0],x_vals[:,1],'*-')
for i in range(num_obst):
    plt.fill(obsVerts[i][0,:],obsVerts[i][1,:],'r')
plt.plot([-boundaryRHS[0,0], boundaryRHS[2,0], boundaryRHS[2,0], -boundaryRHS[0,0], -boundaryRHS[0,0]], [-boundaryRHS[1,0], -boundaryRHS[1,0], boundaryRHS[3,0], boundaryRHS[3,0], -boundaryRHS[1,0]])
plt.plot([-targetRHS[0,0], targetRHS[2,0], targetRHS[2,0], -targetRHS[0,0], -targetRHS[0,0]], [-targetRHS[1,0], -targetRHS[1,0], targetRHS[3,0], targetRHS[3,0], -targetRHS[1,0]])
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.axis('scaled')
plt.show()
