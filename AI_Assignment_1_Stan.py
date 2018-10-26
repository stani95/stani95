import numpy as np
import copy
import time


#A Priority Queue Class:
class PQ:

	#The Priority Queue (PQ) has a list of priorities (numbers) and a list of elements (states).
	#The i-th priority corresponds to the i-th element.
	#Lower priority elements are pop-ed first:
	def __init__(self, priorities, elements):
		self.priorities = priorities
		self.elements = elements

	#A pop method:
	def pop(self):
		if self.empty():
			print "Cannot pop from empty PQ"
			return -1
		else:    #If the PQ is not empty:

			#Find the index of the element with the smallest priority:
			index_to_pop = self.priorities.index(min(self.priorities))

			#The relevant [priority, element] pair to return:
			to_return = [self.priorities[index_to_pop], self.elements[index_to_pop]]

			#Remove it from the list of elements:
			self.elements = self.elements[:index_to_pop]+self.elements[index_to_pop+1:]

			#Remove it from the list of priorities:
			self.priorities = self.priorities[:index_to_pop]+self.priorities[index_to_pop+1:]

			return to_return    #Return that pair.

	#Add a [priority, element] pair to the PQ:
	def add(self, to_add):
		self.elements.append(to_add[1])
		self.priorities.append(to_add[0])

	#Given a board state "to_search", find the index in the PQ
	#of the element that has this board state
	def search_for_index(self, to_search):
		for i in range(len(self.elements)):

			#If the board state of the i-th element coincides with the one we need, return i:
			if self.elements[i].get_state() == to_search:
				return i
		return "ERROR"

	#Given a board state "to_search", find whether there is an
	#element in the PQ that has this board state
	def search_general(self, to_search):
		for i in self.elements:

			#If the board state of the element coincides with the one we need, return True:
			if i.get_state() == to_search:
				return True
		return False

	#Pop a [priority, element] pair with a specific index from the PQ:
	def remove_index(self, index_to_remove):

		#The relevant [priority, element] pair to return:
		to_return = [self.priorities[index_to_remove], self.elements[index_to_remove]]

		#Remove it from the list of elements:
		self.elements = self.elements[:index_to_remove]+self.elements[index_to_remove+1:]

		#Remove it from the list of priorities:
		self.priorities = self.priorities[:index_to_remove]+self.priorities[index_to_remove+1:]

		return to_return    #Return that pair.

	#Get a [priority, element] pair with a specific index from the PQ, without popping it:
	def get_from_index(self, index_to_get):
		return [self.priorities[index_to_get], self.elements[index_to_get]]

	#Given a board state "state", find the steps_to_node of the element
	#that has this board state in the PQ
	def get_steps_from_state(self, state):
		for i in self.elements:

			#If the board state of the element coincides with the one we need, return steps_to_node:
			if i.get_state() == state:
				return i.get_steps_to_node()

		return "ERROR"

	#Get the length of the PQ:
	def length(self):
		return len(self.elements)

	#Check if the PQ is empty:
	def empty(self):
		return len(self.elements) == 0

	#Print the contents of the PQ
	#For the elements, I print the board state and the number of steps from the initial node:
	def print_PQ(self):
		for i in range(len(self.elements)):
			print self.priorities[i], self.elements[i].get_state(), self.elements[i].get_steps_to_node()



class PuzzleNode:

	def __init__(self, n, state, parent = None, steps_to_node = 0, parent_direction = None):

		#The size of the board
		self.n = n

		#The state of the board as a list of lists (n x n)
		self.state = state

		#A pointer to the parent node
		self.parent = parent

		#The number of steps from the initial state to this one
		self.steps_to_node = steps_to_node

		#Where is the parent located relative to this node (left,right,up,down)
		self.parent_direction = parent_direction

	#Move the '0' tile in some direction (left,right,up,down)
	def move(self, direction):

		#A list of valid directions:
		if direction in ['l', 'r', 'u', 'd']:

			#Find the coordinates of the '0' tile:
			for i in range(self.n):
				if 0 in self.state[i]:
					tile_x = i    #Index of the row where '0' is
					tile_y = self.state[i].index(0)    #Index of the column where '0' is

			#We cannot move outside the boundaries of the board:
			if direction == 'l' and tile_y == 0:
				return -1
			if direction == 'r' and tile_y == self.n-1:
				return -1
			if direction == 'u' and tile_x == 0:
				return -1
			if direction == 'd' and tile_x == self.n-1:
				return -1

			#The state to return is a modified coly of the given state:
			new_state = copy.deepcopy(self)

			#Its parent is the given state:
			new_state.set_parent(self)

			#We did a move, so we increment the number of steps from the initial state:
			new_state.set_steps_to_node(self.steps_to_node+1)

			#A copy of the current state of the board, which we can modify and assign
			#as the state of the board after the move:
			state_to_assign = [i for i in new_state.get_state()]

			#For each direction, swap the '0' tile and the one next to it in the relevant direction.
			#Then assign that new state of the board using set_state.
			#Finally, indicate the direction of the parent, relative to the new state:
			if direction == 'l':
				state_to_assign[tile_x][tile_y], state_to_assign[tile_x][tile_y-1] = state_to_assign[tile_x][tile_y-1], state_to_assign[tile_x][tile_y]
				new_state.set_state(state_to_assign)
				new_state.set_parent_direction('r')
			if direction == 'r':
				state_to_assign[tile_x][tile_y], state_to_assign[tile_x][tile_y+1] = state_to_assign[tile_x][tile_y+1], state_to_assign[tile_x][tile_y]
				new_state.set_state(state_to_assign)
				new_state.set_parent_direction('l')
			if direction == 'u':
				state_to_assign[tile_x][tile_y], state_to_assign[tile_x-1][tile_y] = state_to_assign[tile_x-1][tile_y], state_to_assign[tile_x][tile_y]
				new_state.set_state(state_to_assign)
				new_state.set_parent_direction('d')
			if direction == 'd':
				state_to_assign[tile_x][tile_y], state_to_assign[tile_x+1][tile_y] = state_to_assign[tile_x+1][tile_y], state_to_assign[tile_x][tile_y]
				new_state.set_state(state_to_assign)
				new_state.set_parent_direction('u')

			#Return the modified copy of the state:
			return new_state

		#If the direction given to the function was not a valid direction:
		else:
			return -1

	#The printing function. It works for 2 <= n <= 10.
	def str(self):
		for i in range(self.n):
			print "",
			for j in range(self.n-1):
				print "----",
			print "----"
			print "|",
			for j in range(self.n-1):
				if self.state[i][j] < 10:
					print "", self.state[i][j], "|",
				else:
					print self.state[i][j], "|",
			if self.state[i][self.n-1] < 10:
				print "", self.state[i][self.n-1], "|"
			else:
				print self.state[i][self.n-1], "|"
		print "",
		for j in range(self.n):
			print "----",
		print '\n'

	#Get the parent of the current node:
	def get_parent(self):
		return self.parent

	#Set the parent of the current node:
	def set_parent(self, parent):
		self.parent = parent

	#Get the state of the board of the current node:
	def get_state(self):
		return self.state

	#Set the state of the board of the current node:
	def set_state(self, state):
		self.state = state

	#Get the number of steps to get to the node from the initial state:
	def get_steps_to_node(self):
		return self.steps_to_node

	#Set the number of steps to get to the node from the initial state:
	def set_steps_to_node(self, steps_to_node):
		self.steps_to_node = steps_to_node

	#Get the direction of the parent relative to the current state:
	def get_parent_direction(self):
		return self.parent_direction

	#Set the direction of the parent relative to the current state:
	def set_parent_direction(self, parent_direction):
		self.parent_direction = parent_direction


#The first heuristic function - Number of misplaced tiles:
def h1(state):
	num_misplaced = 0    #The current number of misplaced tiles.
	solved_value = 0    #The correct value at the current position.
	for i in state:
		for j in i:     # j = The tile number standing at the current position.

			#Only checking non-zero tiles if they are at the correct position:
			if j != solved_value and j!=0:
				num_misplaced += 1    #Not in the correct position

			#Moving to the next correct value, as we change the position
			solved_value += 1

	return num_misplaced    #Return the number of misplaced tiles

#The second heuristic function - Manhattan distance:
def h2(state):
	manh_sum = 0    #The current value for the Manhattan distance.
	n = len(state)    #The size of the board.
	for i in range(n):
		for j in range(n):

			#Update the Manhattan distance for each square containing a non-zero tile:
			if state[i][j] != 0:

				# state[i][j]%n is the index of the correct column for that tile.
				# state[i][j]/n is the index of the correct row for that tile.
				#Summing up the absolute values of the differences between the
				#correct row/column and the current row/column gives the Manhattan update:
				manh_sum += abs(state[i][j]%n-j)+abs(state[i][j]/n-i)

	return manh_sum    #Return the Manhattan distance

#The third heuristic function - Manhattan distance with a pattern database:
# IT ONLY WORKS FOR N=3 !
def h3(state):

	#If the current state is in the database of true distances to the goal:
	if state in list(np.array(heuristic_list)[:,0]):
		#Return the true distance for that state by looking up in the database:
		return list(np.array(heuristic_list)[:,1])[list(np.array(heuristic_list)[:,0]).index(state)]

	#If the current state is NOT in the database of true distances to the goal,
	#just use the Manhattan distance instead.
	else:
		manh_sum = 0
		n = len(state)
		for i in range(n):
			for j in range(n):
				if state[i][j] != 0:
					manh_sum += abs(state[i][j]%n-j)+abs(state[i][j]/n-i)
		return manh_sum

#The list of heuristics:
heuristics = [h1, h2, h3]


#Checks the format of the board - whether it is (n x n) and whether it contains
#all numbers from 0 to n^2-1 exactly once.
def check_format(state, n):

	#Checking the number of rows:
	if n != len(state):
		return -1

	#Checking the number of squares in each row:
	for i in state:
		if n != len(i):
			return -1

	#A set of all numbers on the board:
	all_numbers = set([i for j in state for i in j])

	#A set of all numbers from 0 to n^2-1:
	true_numbers = set([i for i in range(n*n)])

	#Check if the two sets coincide:
	if all_numbers != true_numbers:
		return -1
	return 1



#Solving the Puzzle with A*:
def solvePuzzle(n, state, heuristic, prnt):

	#Checking the format of the board:
	if check_format(state, n) == -1:
		return 0, 0, -1

	#Checking if the state is solvable:
	flattened_to_sort = [i for j in state for i in j]    #A flattened list of the states
	index_of_zero = flattened_to_sort.index(0)    #The index of the '0' tile in that list
	parity = 0

	#We sort the array by putting the tile 'i' in the i-th position at the i-th step by swapping:
	for j in range(n*n):
		if flattened_to_sort[j]!=j:
			flattened_to_sort[flattened_to_sort.index(j)], flattened_to_sort[j] = flattened_to_sort[j], flattened_to_sort[flattened_to_sort.index(j)]
			parity+=1

	#parity now contains the number of swaps, hence its parity gives the parity of the permutation:
	parity = parity%2

	#The manhattan distance of the '0' tile to its correct position
	manh = index_of_zero%n+index_of_zero/n
	manh = manh%2    #The parity of that Manhattan distance

	#The sum of the two parities gives an indicator of whether the state is solvable:
	solvable = 1-((parity+manh)%2)

	if solvable == 0:
		return 0, 0, -2    #If it is not solvable, return -2.

	#If it is solvable, proceed to solving it:
	else:

		goal_reached = False    #Indicates whether we have reached the goal state:
		puzzle = PuzzleNode(n, state)    #Creating the initial board

		#I will keep the frontier in a priority queue that I implemented:
		frontier = PQ([],[])

		#Adding the initial state to the frontier:
		frontier.add([heuristic(puzzle.get_state())+puzzle.get_steps_to_node(),puzzle])

		max_frontier_size = 1    #Keeps track of the max frontier size so far

		#A list of the board states of all visited nodes:
		all_visited_states = [puzzle.get_state()]

		#Since the state is always solvable, we must have either reached the goal state
		#or have more nodes in the frontier to explore:
		while frontier.empty() == False and goal_reached == False:

			#Pop the element in the frontier with the lowest priority to expand:
			to_expand = frontier.pop()[1]

			#Check if we have reached the goal state. If yes, break the loop:
			if to_expand.get_state()==[[i*n+j for j in range(n)] for i in range(n)]:
				goal_reached = True
				break

			dir_list = ['l', 'r', 'u', 'd']    #['left', 'right', 'up', 'down']

			#Remove the direction of the parent - so not to repeat the previous state:
			if to_expand.get_parent_direction() != None:
				dir_list.remove(to_expand.get_parent_direction())

			#Expand the tree possible directions:
			for direction in dir_list:

				#result is the node after moving in the specified direction
				result = to_expand.move(direction)

				if result != -1:    #If the move is valid

					#If that result state is already in the frontier:
					if frontier.search_general(result.get_state()):

						#Check if the new path to that node is shorter than the one previously found:
						if result.get_steps_to_node() < frontier.get_steps_from_state(result.get_state()):

							#Find the index in the Priority Queue that corresponds to the state:
							index_in_PQ = frontier.search_for_index(result.get_state())

							#Pop the [priority, element] pair which has that index:
							element_in_PQ = frontier.remove_index(index_in_PQ)

							#Update the priority by subtracting the old steps_to_node
							#and adding the new (and smaller) steps_to_node:
							element_in_PQ[0] += result.get_steps_to_node() - element_in_PQ[1].get_steps_to_node()

							#Update the element by setting the new (and smaller) steps_to_node:
							element_in_PQ[1].set_steps_to_node(result.get_steps_to_node())

							#Update the element by setting the new parent:
							element_in_PQ[1].set_parent(result.get_parent())

							#Update the element by setting the new parent dirrection:
							element_in_PQ[1].set_parent_direction(result.get_parent_direction())

							#Add the [priority, element] pair to the frontier:
							frontier.add(element_in_PQ)

					#If that result state is NOT already in the frontier:
					elif result.get_state() not in all_visited_states:

						#Add it to the frontier:
						frontier.add([heuristic(result.get_state())+result.get_steps_to_node(),result])

						#Add the state of the board to the list of all visited board states:
						all_visited_states.append(result.get_state())

			#Update the max frontier size:
			max_frontier_size = max(max_frontier_size, frontier.length())

		if goal_reached == True:

			#The total number of steps it took to reach the goal:
			steps_to_return = to_expand.get_steps_to_node()

			#Printing:
			if prnt == True:

				#to_print will contain all nodes on the path to the goal:
				to_print = [to_expand]
				while to_expand.get_steps_to_node() > 0:
					to_expand = to_expand.get_parent()    #Get the parent node
					to_print.append(to_expand)    #Add the parent node to the list

				#Count the number of steps and print all boards from initial to goal state:
				step = 0
				for i in reversed(to_print):
					print "Step =", step
					i.str()
					step += 1

				#Print the results from the search:
				print "Total number of steps:", steps_to_return
				print "Maximum frontier size:", max_frontier_size

			return steps_to_return, max_frontier_size, 0    #Return when success.

		else:
			#This should never happen because the state is always solvable:
			print "Error!"
			return 0, 0, -2



#Example state 1: [[5,7,6],[2,4,3],[8,1,0]]
#Example state 2: [[7,0,8],[4,6,1],[5,3,2]]
#Example state 3: [[2,3,7],[1,8,0],[6,5,4]]


print "Testing Example state 1 with the number of misplaced tiles heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[5,7,6],[2,4,3],[8,1,0]], heuristic = heuristics[0], prnt = True)
end = time.time()
print "err =", err
print "Time to solve Example state 1 using the number of misplaced tiles heuristic:", end - start

print "Testing Example state 1 with the Manhattan heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[5,7,6],[2,4,3],[8,1,0]], heuristic = heuristics[1], prnt = True)
end = time.time()
print "err =", err
print "Time to solve Example state 1 using the Manhattan heuristic:", end - start


print "Testing Example state 2 with the number of misplaced tiles heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[7,0,8],[4,6,1],[5,3,2]], heuristic = heuristics[0], prnt = True)
end = time.time()
print "err =", err
print "Time to solve Example state 2 using the number of misplaced tiles heuristic:", end - start

print "Testing Example state 2 with the Manhattan heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[7,0,8],[4,6,1],[5,3,2]], heuristic = heuristics[1], prnt = True)
end = time.time()
print "err =", err
print "Time to solve Example state 2 using the Manhattan heuristic:", end - start


print "Testing Example state 3 with the number of misplaced tiles heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[2,3,7],[1,8,0],[6,5,4]], heuristic = heuristics[0], prnt = True)
end = time.time()
print "err =", err
print "Time to solve Example state 3 using the number of misplaced tiles heuristic:", end - start

print "Testing Example state 3 with the Manhattan heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[2,3,7],[1,8,0],[6,5,4]], heuristic = heuristics[1], prnt = True)
end = time.time()
print "err =", err
print "Time to solve Example state 3 using the Manhattan heuristic:", end - start







'''
This is the same function as solvePuzzle, but I use it to return the nodes on the way
from the initial state to the goal state. I could not use solvePuzzle for this purpose
because of the requirement in the assignment instructions for the return clause to be
in a specific form: steps, frontierSize, err = solvePuzzle(n, state, heuristic, prnt).

I need these nodes in order to construct the third heuristic function.
'''
def solvePuzzle_for_heuristic(n, state, heuristic, prnt):
	if check_format(state, n) == -1:
		return 0, 0, -1
	flattened_to_sort = [i for j in state for i in j]
	index_of_zero = flattened_to_sort.index(0)
	parity = 0
	for j in range(n*n):
		if flattened_to_sort[j]!=j:
			flattened_to_sort[flattened_to_sort.index(j)], flattened_to_sort[j] = flattened_to_sort[j], flattened_to_sort[flattened_to_sort.index(j)]
			parity+=1
	parity = parity%2
	manh = index_of_zero%n+index_of_zero/n
	manh = manh%2
	solvable = 1-((parity+manh)%2)
	if solvable == 0:
		return 0, 0, -2
	else:
		goal_reached = False
		puzzle = PuzzleNode(n, state)
		frontier = PQ([],[])
		frontier.add([heuristic(puzzle.get_state())+puzzle.get_steps_to_node(),puzzle])
		max_frontier_size = 1
		all_visited_states = [puzzle.get_state()]
		while frontier.empty() == False and goal_reached == False:
			to_expand = frontier.pop()[1]
			if to_expand.get_state()==[[i*n+j for j in range(n)] for i in range(n)]:
				goal_reached = True
				break
			dir_list = ['l', 'r', 'u', 'd']
			if to_expand.get_parent_direction() != None:
				dir_list.remove(to_expand.get_parent_direction())
			for direction in dir_list:
				result = to_expand.move(direction)
				if result != -1:
					if frontier.search_general(result.get_state()):
						if result.get_steps_to_node() < frontier.get_steps_from_state(result.get_state()):
							index_in_PQ = frontier.search_for_index(result.get_state())
							element_in_PQ = frontier.remove_index(index_in_PQ)
							element_in_PQ[0] += result.get_steps_to_node() - element_in_PQ[1].get_steps_to_node()
							element_in_PQ[1].set_steps_to_node(result.get_steps_to_node())
							element_in_PQ[1].set_parent(result.get_parent())
							element_in_PQ[1].set_parent_direction(result.get_parent_direction())
							frontier.add(element_in_PQ)
					elif result.get_state() not in all_visited_states:
						frontier.add([heuristic(result.get_state())+result.get_steps_to_node(),result])
						all_visited_states.append(result.get_state())

			max_frontier_size = max(max_frontier_size, frontier.length())

		if goal_reached == True:
			steps_to_return = to_expand.get_steps_to_node()
			if prnt == True:
				to_print = [to_expand]
				while to_expand.get_steps_to_node() > 0:
					to_expand = to_expand.get_parent()
					to_print.append(to_expand)
				step = 0
				for i in reversed(to_print):
					#print "Step =", step
					#i.str()
					step += 1
				#print "Total number of steps:", steps_to_return
				#print "Maximum frontier size:", max_frontier_size

			#Here is the main difference with solvePuzzle (returning to_print):
			return steps_to_return, max_frontier_size, 0, to_print
		else:
			print "Error!"
			return 0, 0, -2




'''
This code is for building the pattern database for the third heuristic
'''
i = 0    #Number of initial states to solve

#In heuristic_list, I will keep pairs of the type [board state, distance to goal],
#where distance to goal is the true distance from the board state to the goal state:
heuristic_list = []

while i < 200:    #I will solve 199 random initial states

	#Choose a random permutation of (1,2,...,9) for the initial state:
	perm_to_sort = np.random.permutation(9)
	perm_to_sort = [j for j in perm_to_sort]
	perm = [j for j in perm_to_sort]

	#As in solvePuzzle, check the random state for solvability:
	index_of_zero = perm_to_sort.index(0)
	parity = 0
	for j in range(9):
		if perm_to_sort[j]!=j:
			perm_to_sort[perm_to_sort.index(j)], perm_to_sort[j] = perm_to_sort[j], perm_to_sort[perm_to_sort.index(j)]
			parity+=1
	parity = parity%2
	manh = index_of_zero%3+index_of_zero/3
	manh = manh%2
	solvable = 1-((parity+manh)%2)

	if solvable == 1:    #If the random state is solvable:

		print "Random initial state number", i
		print "Number of solved states =", len(heuristic_list)    #Printint the number of solved states

		i+=1
		if i==1:    #The first time, solve the puzzle with the Manhattan heuristic:
			steps, frontierSize, err, parents_list = solvePuzzle_for_heuristic( n = 3, state = [[perm[k+3*j] for k in range(3)] for j in range(3)], heuristic = heuristics[1], prnt = True)
		else:    #For all other times, use the new third heuristic to solve the puzzle:
			steps, frontierSize, err, parents_list = solvePuzzle_for_heuristic( n = 3, state = [[perm[k+3*j] for k in range(3)] for j in range(3)], heuristic = heuristics[2], prnt = True)
		if err == -2:
			print "ERROR"    #We should never get that because we have ensured that the state is solvable.
		else:

			#Take the list of all nodes from the initial state to the goal state.
			#Assign their respective distances to the goal (e.g. assign 0 to the goal state).
			#Finally, add the board states and their corresponding assignments to heuristic_list.
			while len(parents_list)>0:
				parent_state = parents_list.pop()
				if i == 1:
					heuristic_list.append([parent_state.get_state(), steps - parent_state.get_steps_to_node()])
				else:
					#After the first time, check if the board state is not already in heuristic_list:
					if parent_state.get_state() not in list(np.array(heuristic_list)[:,0]):
						heuristic_list.append([parent_state.get_state(), steps - parent_state.get_steps_to_node()])


print "The number of fully solved states to use in the heuristic is:", len(heuristic_list)

print "Solving Example state 1 using the third custom heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[5,7,6],[2,4,3],[8,1,0]], heuristic = heuristics[2], prnt = True)
end = time.time()
print "Time to solve Example state 1 using the third custom heuristic:", end - start

print "Solving Example state 2 using the third custom heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[7,0,8],[4,6,1],[5,3,2]], heuristic = heuristics[2], prnt = True)
end = time.time()
print "Time to solve Example state 2 using the third custom heuristic:", end - start

print "Solving Example state 3 using the third custom heuristic:"
start = time.time()
steps, frontierSize, err = solvePuzzle( n = 3, state = [[2,3,7],[1,8,0],[6,5,4]], heuristic = heuristics[2], prnt = True)
end = time.time()
print "Time to solve Example state 3 using the third custom heuristic:", end - start
