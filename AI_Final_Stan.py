import random
from copy import deepcopy
#random.seed(1)

#The main class, which contains all the information
#about the agent from its point of view.
class Agent:
	def __init__(self, position = [0,0], orientation = 'right', has_arrow = 1, perception = [[],[]], score = 0, alive = 1, has_gold = 0, KB_pits = [], KB_no_pits = [], KB_wumpus = [], KB_no_wumpus = [], KB2 = [], KB2_no = [], visited = [], killed_wumpus = 0):
		self.position = position             #The current position of the Agent. (e.g. [1,2])
		self.orientation = orientation       #The current orientation of the Agent. (e.g. 'left')
		self.has_arrow = has_arrow           #Binary: Whether the Agent has the arrow ready to shoot (1) or not (0)
		self.perception = perception         #What the agent is currently perceiving. Format is [[...],[...]], where the first list has the cell-specific percepts 'glitter', 'breeze', 'stench', and the second has 'bump' and 'scream'.
		self.score = score                   #The current score of the Agent (-1 per move, -10 per arrow shot, -1000 per death, +1000 for exiting with the gold)
		self.alive = alive                   #Binary: Whether the Agent is alive (1) or not (0)
		self.has_gold = has_gold             #Binary: Whether the Agent has got the gold or not (e.g. 1)
		self.KB_pits = KB_pits               #This is essentially a CNF of the format [[...],[...],[...],...], where each of the lists inside is a disjunction, and the whole list is a conjunction. Each disjunction comes from a 'breeze' perception.
		self.KB_no_pits = KB_no_pits         #This is a conjunction (list) of negated literals that come from the lack of 'breeze' percepts.
		self.KB_wumpus = KB_wumpus           #This is essentially a CNF of the format [[...],[...],[...],...], where each of the lists inside is a disjunction, and the whole list is a conjunction. Each disjunction comes from a 'stench' perception.
		self.KB_no_wumpus = KB_no_wumpus     #This is a conjunction (list) of negated literals that come from the lack of 'stench' percepts.
		self.KB2 = KB2                       #This is an alternative KB of a world in which the wumpus is dead. I update it in parallel with the other one and use it after hearing a 'scream' percept. It comes from 'breeze' perceptions.
		self.KB2_no = KB2_no                 #The other part of the alternative KB - comes from the lack of 'breeze' percepts.
		self.visited = visited               #A list of all visited cells so far
		self.killed_wumpus = killed_wumpus   #Binary: Whether the Wumpus has been killed (1) or not (0)

	#Get the position of the agent
	def get_position(self):
		return self.position

	#Get the orientation of the agent
	def get_orientation(self):
		return self.orientation

	#Get the perception of the agent
	def get_perception(self):
		return self.perception

	#Get the score of the agent
	def get_score(self):
		return self.score

	#Get whether the agent is alive
	def get_alive(self):
		return self.alive

	#Kill the agent ;(
	def kill(self):
		self.alive = 0

	#Add points to the agent's score
	def add_to_score(self, points):
		self.score += points

	#Perceive a perception that is cell-specific
	def perceive(self, perception):
		self.perception[0].append(perception)

	#Resets only the cell-specific perceptions
	def reset_perception(self):
		self.perception[0] = []

	#Removes only the 'stench' perception
	def remove_stench_from_perception(self):
		if 'stench' in self.perception[0]:
			self.perception[0].remove('stench')

	#Perceive a perception that is not cell-specific
	def perceive_temp(self, perception):
		self.perception[1].append(perception)

	#Resets only the non-cell-specific perceptions
	def reset_temp_perception(self):
		self.perception[1] = []

	#Adds the current list of perceptions to the KB
	def add_to_KB(self, perc):
		if self.position not in self.visited:

			#The current position cannot have a pit
			if self.position not in self.KB_no_pits:
				self.KB_no_pits.append(deepcopy(self.position))

			#The current position cannot have a wumpus
			if self.position not in self.KB_no_wumpus:
				self.KB_no_wumpus.append(deepcopy(self.position))

			adjacent_list = list_of_adjacent_cells(self.position)

			#If the agent perceives a breeze, then at least one of its adjacent cells has a pit
			if 'breeze' in perc[0]:
				self.KB_pits.append(deepcopy(adjacent_list))

			#If the agent does not perceive a pit, then all the adjacent cells do not have pits
			else:
				for i in range(len(adjacent_list)):
					if adjacent_list[i] not in self.KB_no_pits:
						self.KB_no_pits.append(deepcopy(adjacent_list[i]))

			#If the agent perceives a stench, then at least one of its adjacent cells has a wumpus
			if 'stench' in perc[0]:
				self.KB_wumpus.append(deepcopy(adjacent_list))

			#If the agent does not perceive a stench, then all the adjacent cells do not have wumpus
			else:
				for i in range(len(adjacent_list)):
					if adjacent_list[i] not in self.KB_no_wumpus:
						self.KB_no_wumpus.append(deepcopy(adjacent_list[i]))

			#If the agent hears a 'scream', then the wumpus is dead
			if 'scream' in perc[1]:
				self.update_kill_wumpus()

	#Same for the alternative KB:
	def add_to_KB2(self, perc):
		if self.position not in self.visited:
			if self.position not in self.KB2_no:
				self.KB2_no.append(deepcopy(self.position))
			adjacent_list = list_of_adjacent_cells(self.position)
			if 'breeze' in perc[0]:
				self.KB2.append(deepcopy(adjacent_list))
			else:
				for i in range(len(adjacent_list)):
					if adjacent_list[i] not in self.KB2_no:
						self.KB2_no.append(deepcopy(adjacent_list[i]))

	#Adds the current position to the list of visited states
	def add_to_visited(self, pos):
		if pos not in self.visited:
			self.visited.append(deepcopy(pos))

	#Get whether the wumpus has been killed
	def get_killed_wumpus(self):
		return self.killed_wumpus

	#If the agent perceives 'scream', then the wumpus has been killed
	def update_kill_wumpus(self, perc):
		if 'scream' in perc[1]:
			self.killed_wumpus = 1

	#Moving forward
	def move_forward(self):

		if self.orientation == 'right':
			if self.position[1] == 3:           #The condition for Bumping
				self.perceive_temp('bump')
				print "BUMP!"
			else:
				self.position[1] += 1           #If there is no Bumping

		if self.orientation == 'left':
			if self.position[1] == 0:
				self.perceive_temp('bump')
				print "BUMP!"
			else:
				self.position[1] -= 1

		if self.orientation == 'up':
			if self.position[0] == 0:
				self.perceive_temp('bump')
				print "BUMP!"
			else:
				self.position[0] -= 1

		if self.orientation == 'down':
			if self.position[0] == 3:
				self.perceive_temp('bump')
				print "BUMP!"
			else:
				self.position[0] += 1

	#Agent turns left and changes its orientation
	def turn_left(self):
		if self.orientation == 'right':
			self.orientation = 'up'
		elif self.orientation == 'up':
			self.orientation = 'left'
		elif self.orientation == 'left':
			self.orientation = 'down'
		elif self.orientation == 'down':
			self.orientation = 'right'

	#Agent turns right and changes its orientation
	def turn_right(self):
		if self.orientation == 'right':
			self.orientation = 'down'
		elif self.orientation == 'down':
			self.orientation = 'left'
		elif self.orientation == 'left':
			self.orientation = 'up'
		elif self.orientation == 'up':
			self.orientation = 'right'

	#The agent can shoot the arrow only if it still has it
	def shoot_arrow(self):
		if self.has_arrow == 0:
			print "CANNOT SHOOT ARROW!"
			return -1
		else:
			self.has_arrow = 0
			return 1

	#The human Wumpus game interface: Choose a letter to make a move!
	def decide_action_human(self):
		my_action = raw_input("Please select an action: (f, l, r, g, e, s): ")
		return my_action

	#This function finds a sequence of adjacent and safe cells from a start point to a goal point (goal is not necessarily safe).
	def find_path_to_goal(self, current, goal, available):
		available_copy = deepcopy(available)                #A list of cells available for movement (safe cells)
		current_cell = deepcopy(current[-1])
		adjacent = list_of_adjacent_cells(current[-1])

		for i in adjacent:
			if i == goal:
				current.append(i)
				return current, True                   #Return the list of cells + True if goal is reached

		for i in adjacent:
			if i in available_copy:
				available_copy.remove(current[-1])
				current_copy = deepcopy(current[-1])   #Do a recursion if the goal is still not reached.
				current.append(i)                      
				path_find = self.find_path_to_goal(deepcopy(current), goal, available_copy)

				if path_find[1] == True:
					return path_find
				else:
					available_copy.append(current_copy)
					current.remove(i)

		return [], False

	#Returns a sequence of actions (e.g. ['f','r','f','e']) that achieve a goal.
	def actions_to_reach_goal(self, goal):

		if self.position == goal:
			print "EXIT CAVE!"
			return ['e']			#This can only happen in the (0,0) cell.

		path_to_goal = self.find_path_to_goal([self.position], goal, self.visited)[0]
		instructions_to_reach_goal = []
		cur_orientation = self.orientation    #Current orientation

		for i in range(len(path_to_goal)-1):                    #Traversing the path using the available actions.
			if path_to_goal[i+1][0]-path_to_goal[i][0] == 1:    #If the next cell is down from the current cell
				if cur_orientation == 'down':
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'up':
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'right':
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				else:
					instructions_to_reach_goal.append('l')
					instructions_to_reach_goal.append('f')
				cur_orientation = 'down'
			if path_to_goal[i+1][0]-path_to_goal[i][0] == -1:    #If the next cell is up from the current cell
				if cur_orientation == 'up':
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'down':
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'right':
					instructions_to_reach_goal.append('l')
					instructions_to_reach_goal.append('f')
				else:
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				cur_orientation = 'up'
			if path_to_goal[i+1][1]-path_to_goal[i][1] == 1:    #If the next cell is right from the current cell
				if cur_orientation == 'right':
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'left':
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'up':
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				else:
					instructions_to_reach_goal.append('l')
					instructions_to_reach_goal.append('f')
				cur_orientation = 'right'
			if path_to_goal[i+1][1]-path_to_goal[i][1] == -1:    #If the next cell is left from the current cell
				if cur_orientation == 'left':
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'right':
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				elif cur_orientation == 'up':
					instructions_to_reach_goal.append('l')
					instructions_to_reach_goal.append('f')
				else:
					instructions_to_reach_goal.append('r')
					instructions_to_reach_goal.append('f')
				cur_orientation = 'left'

		return instructions_to_reach_goal

	#What actions to take if the goal is to kill the wumpus. Thus can only happen if the agent does not have any other choice (see the manual_setup simulation):
	def actions_to_kill_wumpus(self):

		for m in range(4):
			for n in range(4):
				s_p, dh_p, s_w, dh_w = self.resolution([m,n])    #These are safe_from_pit, definitely_has_pit, safe_from_wumpus, definitely_has_wumpus
				if dh_w:                                         #If we are 100% certain where the wumpus is
					for l in list_of_adjacent_cells([m,n]):
						if l in self.visited:
							if self.position == l:
								if m-l[0] == 1:
									if self.orientation == 'down':
										return ['s']
									elif self.orientation == 'up':
										return ['r','r','s']
									elif self.orientation == 'right':
										return ['r','s']
									else:
										return ['l','s']
								if m-l[0] == -1:
									if self.orientation == 'up':
										return ['s']
									elif self.orientation == 'down':
										return ['r','r','s']
									elif self.orientation == 'right':
										return ['l','s']
									else:
										return ['r','s']
								if n-l[1] == 1:
									if self.orientation == 'right':
										return ['s']
									elif self.orientation == 'left':
										return ['r','r','s']
									elif self.orientation == 'up':
										return ['r','s']
									else:
										return ['l','s']
								if n-l[1] == -1:
									if self.orientation == 'left':
										return ['s']
									elif self.orientation == 'right':
										return ['r','r','s']
									elif self.orientation == 'up':
										return ['l','s']
									else:
										return ['r','s']
							else:
								return self.actions_to_reach_goal(l)



		for m in range(4):
			for n in range(4):
				s_p, dh_p, s_w, dh_w = self.resolution([m,n])
				if not s_w:                                             #If we conjecture that there might be a wumpus in the cell
					for l in list_of_adjacent_cells([m,n]):
						if l in self.visited:
							if self.position == l:
								if m-l[0] == 1:
									if self.orientation == 'down':
										return ['s']
									elif self.orientation == 'up':
										return ['r','r','s']
									elif self.orientation == 'right':
										return ['r','s']
									else:
										return ['l','s']
								if m-l[0] == -1:
									if self.orientation == 'up':
										return ['s']
									elif self.orientation == 'down':
										return ['r','r','s']
									elif self.orientation == 'right':
										return ['l','s']
									else:
										return ['r','s']
								if n-l[1] == 1:
									if self.orientation == 'right':
										return ['s']
									elif self.orientation == 'left':
										return ['r','r','s']
									elif self.orientation == 'up':
										return ['r','s']
									else:
										return ['l','s']
								if n-l[1] == -1:
									if self.orientation == 'left':
										return ['s']
									elif self.orientation == 'right':
										return ['r','r','s']
									elif self.orientation == 'up':
										return ['l','s']
									else:
										return ['r','s']
							else:
								return actions_to_reach_goal(l)

	#If the wumpus is alive, this function chooses which cell to be the next to explore,
	#based on 4 lists - the cells that we are certain are pit-free and wumpus-free, and
	#the ones that we are not sure, which the agent only accesses if the other list is empty.
	def decide_actions_AI_with_wumpus(self):

		#For the GOLD:
		goal_is_to_exit = False
		if ('glitter' in self.perception[0]) and self.has_gold == 0:
			my_actions = ['g']
			goal_is_to_exit = True
		if self.has_gold == 1:
			my_actions = self.actions_to_reach_goal([0,0])
			goal_is_to_exit = True

		if goal_is_to_exit == False:

			#Defining the safe lists:
			safe_cells = [[0 for j in range(4)] for i in range(4)]
			dangerous_cells = [[0 for j in range(4)] for i in range(4)]
			for m in range(4):
				for n in range(4):
					s_p, dh_p, s_w, dh_w = self.resolution([m,n])
					if s_p and s_w:
						safe_cells[m][n] = 1
					if dh_p or dh_w:
						dangerous_cells[m][n] = 1

			#Defining the not-sure-if-safe cells:
			list_of_potential_safe_next_cells = []
			list_of_potential_not_dangerous_next_cells = []

			for m in list_of_potential_next_cells(self.visited):
				if safe_cells[m[0]][m[1]]:
					list_of_potential_safe_next_cells.append(m)
			for m in list_of_potential_next_cells(self.visited):
				if not dangerous_cells[m[0]][m[1]]:
					list_of_potential_not_dangerous_next_cells.append(m)

			#Choosing the safe cells:
			if len(list_of_potential_safe_next_cells) > 0:
				my_actions = self.actions_to_reach_goal(list_of_potential_safe_next_cells[0])
			else:
				#Choosing the not-sure cells:
				if len(list_of_potential_not_dangerous_next_cells) > 0:
					my_actions = self.actions_to_reach_goal(list_of_potential_not_dangerous_next_cells[0])
				#Only if we are sure that all the unexplored squares contain pits and wumpuses, we can try to kill the wumpus (see manual_setup)
				elif self.killed_wumpus == 0 and self.has_arrow == 1:
					my_actions = self.actions_to_kill_wumpus()
				else:
					print "AGENT HAS NO VIABLE MOVE!"
					my_actions = ['f']

			return my_actions
		else:
			#To exit the game:
			return my_actions

	#Same as above for the alternative KB:
	def decide_actions_AI_without_wumpus(self):
		goal_is_to_exit = False
		if ('glitter' in self.get_perception()) and self.has_gold == 0:
			my_actions = ['g']
			goal_is_to_exit = True
		if self.has_gold == 1:
			goal_is_to_exit = True

		if goal_is_to_exit == False:
			safe_cells = [[0 for j in range(4)] for i in range(4)]
			dangerous_cells = [[0 for j in range(4)] for i in range(4)]
			for m in range(4):
				for n in range(4):
					s_p, dh_p, s_w, dh_w = self.resolution([m,n])
					if s_p and s_w:
						safe_cells[m][n] = 1
					if dh_p or dh_w:
						dangerous_cells[m][n] = 1

			list_of_potential_safe_next_cells = []
			list_of_potential_not_dangerous_next_cells = []

			for m in list_of_potential_next_cells(self.visited):
				if safe_cells[m[0]][m[1]]:
					list_of_potential_safe_next_cells.append(m)
			for m in list_of_potential_next_cells(self.visited):
				if not dangerous_cells[m[0]][m[1]]:
					list_of_potential_not_dangerous_next_cells.append(m)

			if len(list_of_potential_safe_next_cells) > 0:
				my_actions = self.actions_to_reach_goal(list_of_potential_safe_next_cells[0])
			else:
				if len(list_of_potential_not_dangerous_next_cells) > 0:
					my_actions = self.actions_to_reach_goal(list_of_potential_not_dangerous_next_cells[0])
				else:
					print "AGENT HAS NO VIABLE MOVE!"
					my_actions = ['f']

			return my_actions
		else:
			#To exit the game:
			return self.actions_to_reach_goal([0,0])

	#To exit the cave from (0,0)
	def exit_cave(self):
		if self.position == [0,0]:
			self.kill()
			if self.has_gold == 1:
				self.score += 1000
			return 1
		else:
			print "Cannot exit cave! Go to cell [0,0] first!"
			return -1

	#To grab the gold where there is 'glitter'
	def grab_gold(self):
		if 'glitter' in self.perception[0]:
			print "GOT THE GOLD!"
			self.has_gold = 1
		else:
			print "Cannot get gold. No gold in this cell."

	#The modified resolution algorithm:
	def resolution(self, to_infer):

		#In the case when the wumpus has been killed:
		if self.killed_wumpus:
			safe_from_pits = False
			definitely_has_a_pit = False

			KB2_no_copy = deepcopy(self.KB2_no)
			KB2_copy = deepcopy(self.KB2)
			KB2_copy.append([to_infer])

			#The resolution. This tries to prove that a cell does not have a pit.
			for i in KB2_no_copy:
				for j in KB22_copy:
					if i in j:
						j.remove(i)
			for j in KB2_copy:
				if len(j)==0:
					safe_from_pits = True

			KB2_no_copy2 = deepcopy(self.KB2_no)
			KB2_copy2 = deepcopy(self.KB2)
			KB2_no_copy2.append(to_infer)

			#The resolution. This tries to prove that a cell has a pit.
			for i in KB2_no_copy2:
				for j in KB2_copy2:
					if i in j:
						j.remove(i)
			for j in KB2_copy2:
				if len(j)==0:
					definitely_has_a_pit = True

			return safe_from_pits, definitely_has_a_pit, True, False

		#In the case when the wumpus is alive:
		else:
			safe_from_pits = False
			definitely_has_a_pit = False

			KB_no_pits_copy = deepcopy(self.KB_no_pits)
			KB_pits_copy = deepcopy(self.KB_pits)
			KB_pits_copy.append([to_infer])

			#The resolution. This tries to prove that a cell does not have a pit.
			for i in KB_no_pits_copy:
				for j in KB_pits_copy:
					if i in j:
						j.remove(i)
			for j in KB_pits_copy:
				if len(j)==0:
					safe_from_pits = True

			KB_no_pits_copy2 = deepcopy(self.KB_no_pits)
			KB_pits_copy2 = deepcopy(self.KB_pits)
			KB_no_pits_copy2.append(to_infer)

			#The resolution. This tries to prove that a cell has a pit.
			for i in KB_no_pits_copy2:
				for j in KB_pits_copy2:
					if i in j:
						j.remove(i)
			for j in KB_pits_copy2:
				if len(j)==0:
					definitely_has_a_pit = True

			safe_from_wumpus = False
			definitely_has_a_wumpus = False

			KB_no_wumpus_copy = deepcopy(self.KB_no_wumpus)
			KB_wumpus_copy = deepcopy(self.KB_wumpus)
			KB_wumpus_copy.append([to_infer])

			#The resolution. This tries to prove that a cell does not have a wumpus.
			for i in KB_no_wumpus_copy:
				for j in KB_wumpus_copy:
					if i in j:
						j.remove(i)
			for j in KB_wumpus_copy:
				if len(j)==0 or (len(j)==1 and (to_infer not in j)):
					safe_from_wumpus = True

			KB_no_wumpus_copy2 = deepcopy(self.KB_no_wumpus)
			KB_wumpus_copy2 = deepcopy(self.KB_wumpus)
			KB_no_wumpus_copy2.append(to_infer)

			#The resolution. This tries to prove that a cell has a wumpus.
			for i in KB_no_wumpus_copy2:
				for j in KB_wumpus_copy2:
					if i in j:
						j.remove(i)
			for j in KB_wumpus_copy2:
				if len(j)==0:
					definitely_has_a_wumpus = True

			return safe_from_pits, definitely_has_a_pit, safe_from_wumpus, definitely_has_a_wumpus

#The list of adjacent cells to a cell:
def list_of_adjacent_cells(cell):
	if cell == [0,0]:
		return [[0,1],[1,0]]
	elif cell == [0,3]:
		return [[1,3],[0,2]]
	elif cell == [3,0]:
		return [[3,1],[2,0]]
	elif cell == [3,3]:
		return [[2,3],[3,2]]
	elif cell[0] == 0:
		return [[0,cell[1]-1],[1,cell[1]],[0,cell[1]+1]]
	elif cell[0] == 3:
		return [[3,cell[1]-1],[2,cell[1]],[3,cell[1]+1]]
	elif cell[1] == 0:
		return [[cell[0]-1,0],[cell[0],1],[cell[0]+1,0]]
	elif cell[1] == 3:
		return [[cell[0]-1,3],[cell[0],2],[cell[0]+1,3]]
	else:
		return [[cell[0]-1,cell[1]],[cell[0]+1,cell[1]],[cell[0],cell[1]-1],[cell[0],cell[1]+1]]

#Given a set of visited cells, these are the cells that are directly accessable by the agent:
def list_of_potential_next_cells(visited_list):
	list_to_return = []
	for i in visited_list:
		for j in list_of_adjacent_cells(i):
			if (j not in visited_list) and (j not in list_to_return):
				list_to_return.append(j)
	return list_to_return

#The usual setup of the board - for a randomized level:
def setup():
	gold_x = random.randint(0,3)
	if gold_x == 0:
		gold = [gold_x,random.randint(1,3)]
	else:
		gold = [gold_x,random.randint(0,3)]

	wumpus_x = random.randint(0,3)
	if wumpus_x == 0:
		wumpus = [wumpus_x,random.randint(1,3)]
	else:
		wumpus = [wumpus_x,random.randint(0,3)]

	pits = [[0 for i in range(4)] for j in range(4)]
	for i in range(4):
		for j in range(4):
			if (i!=0 or j!=0) and gold != [i,j]:
				if random.random()<0.2:
					pits[i][j] = 1

	breezes = [[-1 for i in range(4)] for j in range(4)]
	for i in range(4):
		for j in range(4):
			if pits[i][j] == 1:
				for k in list_of_adjacent_cells([i,j]):
					breezes[k[0]][k[1]] = 1

	stenches = [[-1 for i in range(4)] for j in range(4)]
	for k in list_of_adjacent_cells(wumpus):
		stenches[k[0]][k[1]] = 1

	return gold, wumpus, pits, breezes, stenches

#A manually set up level - one in which the AI agent kills the wumpus and grabs the GOLD!!!
def manual_setup():
	gold = [3,3]
	wumpus = [3,2]

	pits = [[0,0,0,0],[0,0,0,0],[0,0,1,1],[0,0,0,0]]

	breezes = [[-1 for i in range(4)] for j in range(4)]
	for i in range(4):
		for j in range(4):
			if pits[i][j] == 1:
				for k in list_of_adjacent_cells([i,j]):
					breezes[k[0]][k[1]] = 1

	stenches = [[-1 for i in range(4)] for j in range(4)]
	for k in list_of_adjacent_cells(wumpus):
		stenches[k[0]][k[1]] = 1

	return gold, wumpus, pits, breezes, stenches

#Visualizing the cave when the AI is playing (Visualizing the pits, wumpus, and gold)
def visualize_cave(cave, A):
	init_spaces = 6
	print '\n'
	print "  "," "*(init_spaces/2),
	for i in range(4):
		print i, " "*(init_spaces/2+2),
	print '\n'
	print "   ",
	for i in range(4):
		print "-"*(init_spaces+1),
	print '\n'
	for i in range(4):
		print i," |",
		for j in range(4):
			spaces = init_spaces
			if [i,j] == cave[0]:
				print "G",
				spaces -= 2
			if [i,j] == cave[1]:
				print "W",
				spaces -= 2
			if cave[2][i][j] == 1:
				print "P",
				spaces -=2
			if [i,j] == A.get_position():
				if A.get_orientation() == 'right':
					print "AR",
				elif A.get_orientation() == 'left':
					print "AL",
				elif A.get_orientation() == 'up':
					print "AU",
				elif A.get_orientation() == 'down':
					print "AD",
				spaces -=3
			print " "*spaces+"|",
		print '\n'
		print "   ",
		for j in range(4):
			print "-"*(init_spaces+1),
		print '\n'

#Visualizing the cave when the human is playing (Hiding the pits, wumpus, and gold)
def visualize_cave_for_player(cave, A):
	init_spaces = 6
	print '\n'
	print "  "," "*(init_spaces/2),
	for i in range(4):
		print i, " "*(init_spaces/2+2),
	print '\n'
	print "   ",
	for i in range(4):
		print "-"*(init_spaces+1),
	print '\n'
	for i in range(4):
		print i," |",
		for j in range(4):
			spaces = init_spaces
			if [i,j] == A.get_position():
				if A.get_orientation() == 'right':
					print "AR",
				elif A.get_orientation() == 'left':
					print "AL",
				elif A.get_orientation() == 'up':
					print "AU",
				elif A.get_orientation() == 'down':
					print "AD",
				spaces -=3
			print " "*spaces+"|",
		print '\n'
		print "   ",
		for j in range(4):
			print "-"*(init_spaces+1),
		print '\n'

#The AI plays the game:
def play_game_AI():
	A = Agent()

	cave = manual_setup()    #CHANGE THIS TO setup() for the AI to play a random level.

	if A.get_position() == cave[0]:
		A.perceive('glitter')
	if cave[3][A.get_position()[0]][A.get_position()[1]] == 1:
		A.perceive('breeze')
	if cave[4][A.get_position()[0]][A.get_position()[1]] == 1:
		A.perceive('stench')
	print "Perceiving:", A.get_perception()
	A.add_to_KB(A.get_perception())
	A.add_to_KB2(A.get_perception())
	A.add_to_visited(A.get_position())
	print "Score =", A.get_score()

	while A.get_alive() == 1:
		if A.get_killed_wumpus():
			actions = A.decide_actions_AI_without_wumpus()
		else:
			actions = A.decide_actions_AI_with_wumpus()
		A.reset_temp_perception()
		for action in actions:
			visualize_cave(cave, A)
			if action == 'f':
				A.reset_perception()
				A.move_forward()
				if A.get_position() == cave[0]:
					A.perceive('glitter')
				if cave[3][A.get_position()[0]][A.get_position()[1]] == 1:
					A.perceive('breeze')
				if cave[4][A.get_position()[0]][A.get_position()[1]] == 1:
					A.perceive('stench')
				if cave[2][A.get_position()[0]][A.get_position()[1]] == 1:
					A.add_to_score(-1000)
					A.kill()
				if cave[1] == A.get_position():
					A.add_to_score(-1000)
					A.kill()
			elif action == 'l':
				A.turn_left()
			elif action == 'r':
				A.turn_right()
			elif action == 'g':
				A.grab_gold()
			elif action == 'e':
				A.exit_cave()
			elif action == 's':
				if A.shoot_arrow() == 1:
					A.add_to_score(-10)
					cells_hit_by_arrow = []
					if A.get_orientation() == 'right':
						num_of_cells_hit_by_arrow = 3-A.get_position()[1]
						for i in range(num_of_cells_hit_by_arrow):
							cells_hit_by_arrow.append([A.get_position()[0], A.get_position()[1]+i+1])
						if cave[1] in cells_hit_by_arrow:
							A.perceive_temp('scream')
							A.remove_stench_from_perception()
							cave[1][0] = -1
							cave[1][1] = -1
							for i in range(4):
								for j in range(4):
									cave[4][i][j] = -1
					elif A.get_orientation() == 'left':
						num_of_cells_hit_by_arrow = A.get_position()[1]
						for i in range(num_of_cells_hit_by_arrow):
							cells_hit_by_arrow.append([A.get_position()[0], A.get_position()[1]-i-1])
						if cave[1] in cells_hit_by_arrow:
							A.perceive_temp('scream')
							A.remove_stench_from_perception()
							cave[1][0] = -1
							cave[1][1] = -1
							for i in range(4):
								for j in range(4):
									cave[4][i][j] = -1
					elif A.get_orientation() == 'up':
						num_of_cells_hit_by_arrow = A.get_position()[0]
						for i in range(num_of_cells_hit_by_arrow):
							cells_hit_by_arrow.append([A.get_position()[0]-i-1, A.get_position()[1]])
						if cave[1] in cells_hit_by_arrow:
							A.perceive_temp('scream')
							A.remove_stench_from_perception()
							cave[1][0] = -1
							cave[1][1] = -1
							for i in range(4):
								for j in range(4):
									cave[4][i][j] = -1
					else:
						num_of_cells_hit_by_arrow = 3-A.get_position()[0]
						for i in range(num_of_cells_hit_by_arrow):
							cells_hit_by_arrow.append([A.get_position()[0]+i+1, A.get_position()[1]])
						if cave[1] in cells_hit_by_arrow:
							A.perceive_temp('scream')
							A.remove_stench_from_perception()
							cave[1][0] = -1
							cave[1][1] = -1
							for i in range(4):
								for j in range(4):
									cave[4][i][j] = -1
				else:
					A.add_to_score(-1)
					print "Perceiving:", A.get_perception()
					print "Score =", A.get_score()
					A.reset_temp_perception()
					continue
			else:
				print "Invalid action!"

			A.add_to_score(-1)
			if A.get_alive() == 1:
				print "Perceiving:", A.get_perception()
				A.add_to_KB(A.get_perception())
				A.add_to_KB2(A.get_perception())
				A.add_to_visited(A.get_position())
				if 'bump' in A.get_perception()[1]:
					print "THE AI CANNOT SOLVE IT!"
					return 0
				print "Score =", A.get_score()
			else:
				print "Game over! Your score is:", A.get_score()


#A human plays the game (it's fun!)
def play_game_human():
	A = Agent()

	cave = manual_setup()    #CHANGE THIS TO setup() to make a human play a random level.

	if A.get_position() == cave[0]:
		A.perceive('glitter')
	if cave[3][A.get_position()[0]][A.get_position()[1]] == 1:
		A.perceive('breeze')
	if cave[4][A.get_position()[0]][A.get_position()[1]] == 1:
		A.perceive('stench')
	print "Perceiving", A.get_perception()
	print "Score =", A.get_score()
	while A.get_alive() == 1:
		visualize_cave_for_player(cave, A)
		action = A.decide_action_human()
		A.reset_temp_perception()
		if action == 'f':
			A.reset_perception()
			A.move_forward()
			if A.get_position() == cave[0]:
				A.perceive('glitter')
			if cave[3][A.get_position()[0]][A.get_position()[1]] == 1:
				A.perceive('breeze')
			if cave[4][A.get_position()[0]][A.get_position()[1]] == 1:
				A.perceive('stench')
			if cave[2][A.get_position()[0]][A.get_position()[1]] == 1:
				A.add_to_score(-1000)
				A.kill()
			if cave[1] == A.get_position():
				A.add_to_score(-1000)
				A.kill()
		elif action == 'l':
			A.turn_left()
		elif action == 'r':
			A.turn_right()
		elif action == 'g':
			A.grab_gold()
		elif action == 'e':
			A.exit_cave()
		elif action == 's':
			if A.shoot_arrow() == 1:
				A.add_to_score(-10)
				cells_hit_by_arrow = []
				if A.get_orientation() == 'right':
					num_of_cells_hit_by_arrow = 3-A.get_position()[1]
					for i in range(num_of_cells_hit_by_arrow):
						cells_hit_by_arrow.append([A.get_position()[0], A.get_position()[1]+i+1])
					if cave[1] in cells_hit_by_arrow:
						A.perceive_temp('scream')
						A.remove_stench_from_perception()
						cave[1][0] = -1
						cave[1][1] = -1
						for i in range(4):
							for j in range(4):
								cave[4][i][j] = -1
				elif A.get_orientation() == 'left':
					num_of_cells_hit_by_arrow = A.get_position()[1]
					for i in range(num_of_cells_hit_by_arrow):
						cells_hit_by_arrow.append([A.get_position()[0], A.get_position()[1]-i-1])
					if cave[1] in cells_hit_by_arrow:
						A.perceive_temp('scream')
						A.remove_stench_from_perception()
						cave[1][0] = -1
						cave[1][1] = -1
						for i in range(4):
							for j in range(4):
								cave[4][i][j] = -1
				elif A.get_orientation() == 'up':
					num_of_cells_hit_by_arrow = A.get_position()[0]
					for i in range(num_of_cells_hit_by_arrow):
						cells_hit_by_arrow.append([A.get_position()[0]-i-1, A.get_position()[1]])
					if cave[1] in cells_hit_by_arrow:
						A.perceive_temp('scream')
						A.remove_stench_from_perception()
						cave[1][0] = -1
						cave[1][1] = -1
						for i in range(4):
							for j in range(4):
								cave[4][i][j] = -1
				else:
					num_of_cells_hit_by_arrow = 3-A.get_position()[0]
					for i in range(num_of_cells_hit_by_arrow):
						cells_hit_by_arrow.append([A.get_position()[0]+i+1, A.get_position()[1]])
					if cave[1] in cells_hit_by_arrow:
						A.perceive_temp('scream')
						A.remove_stench_from_perception()
						cave[1][0] = -1
						cave[1][1] = -1
						for i in range(4):
							for j in range(4):
								cave[4][i][j] = -1
			else:
				A.add_to_score(-1)
				print "Perceiving:", A.get_perception()
				print "Score =", A.get_score()
				A.reset_temp_perception()
				continue
		else:
			print "Invalid action!"

		A.add_to_score(-1)
		if A.get_alive() == 1:
			print "Perceiving:", A.get_perception()
			print "Score =", A.get_score()
		else:
			print "Game over! Your score is:", A.get_score()


#You can choose who to play by running the code and selecting 'me' or 'AI'
while True:
	player = raw_input("Who is playing? (me, AI) :")
	if player != 'me' and player != 'AI':
		print "Invalid input! Please select from (me,AI)."
	elif player == 'me':
		play_game_human()
		break
	else:
		play_game_AI()
		break

