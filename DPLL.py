import numpy as np

class Literal:

	def __init__(self, name, sign = True):
		self.name = name
		self.sign = sign
		#True means the literal is positive (e.g. A)
		#False means the literal is negative (e.g. -A)

	def __neg__(self):
		return Literal(self.name, bool(1-self.sign))

	def __str__(self):
		return "Name = " + str(self.name) + " and Sign = " + str(self.sign)

	def get_sign(self):
		return self.sign

	def get_name(self):
		return self.name


def DPLLSatisfiable(KB):

	#model is a dictionary. Its keys are the symbols in
	#the KB and the values can be "free", "true", or "false".
	model = {}
	for clause in KB:
		for literal in clause:
			if literal.get_name() not in model.keys():
				model[literal.get_name()] = "free"
				#Initially, all values are "free"

	#degrees is a dictionary. Its keys are the symbols in
	#the KB that are still "free", and the values
	#are the corresponding degrees.
	degrees = {}
	for clause in KB:
		for literal in clause:
			if literal.get_name() not in degrees.keys():
				degrees[literal.get_name()] = 1
			else:
				degrees[literal.get_name()] += 1

	#Run DPLL
	return DPLL(KB, model, degrees)

#TruthValue takes a model and a literal.
def TruthValue(model, literal):

	if (model[literal.get_name()] == 'true' and literal.get_sign() == True) or (model[literal.get_name()] == 'false' and literal.get_sign() == False):
		return True
		#It returns True if the literal is positive and the symbol is assigned True,
		#or if the literal is negative and the symbol is assigned False.

	else:
		return False


#Given a KB and a model, findUnitClause returns
#the literal that corresponds to a unit clause,
#or -1 if such clause does not exist.
def findUnitClause(KB, model):

	for clause in KB:
		number = 0
		unitLiteral = None
		flag = False
		for literal in clause:

			#Ignore all clauses that are True because one of their literals is True:
			if TruthValue(model, literal) == True:
				flag = True
				break

			#Count the number of "free" literals in the clause:
			elif model[literal.get_name()] == 'free':
				number +=1
				unitLiteral = literal

		#If that number is 1, return the literal in that unit Clause:
		if number == 1 and flag == False:
			return unitLiteral

	#If no clauses are unit clauses:
	return -1


#Given a KB and a model, findPureSymbol returns
#a dictionary with sybmols and their signs.
#The signs are positive (True) or negative (False)
#for pure symbols and None for impure symbols.
def findPureSymbol(KB, model):
	signs = {}
	for clause in KB:
		flag = False

		for literal in clause:

			#Ignore all clauses that are True because one of their literals is True:
			if TruthValue(model, literal) == True:
				flag = True
				break
		if flag == True:
			continue

		#Now we are sure that no literals collapse the clause to True:
		for literal in clause:
			if model[literal.get_name()] == 'free':

				#All free literals whose symbol is not yet in the dictionary are added to it:
				if literal.get_name() not in signs.keys():
					signs[literal.get_name()] = literal.get_sign()

				#All free literals whose symbol is already in the dictionary are
				#checked for "purity". If they do not pass the test, I
				#assign None to the corresponding symbol.
				elif literal.get_sign() != signs[literal.get_name()]:
					signs[literal.get_name()] = None

	#Returning the dictionary.
	return signs


#The DPLL function
def DPLL(KB, model, degrees):

	#Check if the current model satisfies the KB:

	#If we do not encounter any 'false' or 'free' clauses in the KB,
	#then all clauses are 'true' and the KB is satisfied.
	flag_KB = 'true'

	for clause in KB:

		#If we do not encounter any 'true' or 'free' literals in the current clause,
		#then all literals are 'false' and the clause is also false.
		flag_clause = 'false'

		for literal in clause:

			#If a literal evaluates to 'true', the whole clause is 'true':
			if TruthValue(model, literal):
				flag_clause = 'true'
				break

			#If at least one literal is 'free', then the clause cannot be 'false':
			if model[literal.get_name()] == 'free':
				flag_clause = 'free'

		#If we did not encounter any 'true' or 'free' literals in the current clause,
		#then all literals are 'false' and the clause is also false. Hence the KB
		#is unsatisfiable under the current model:
		if flag_clause == 'false':
			return False, {}

		#If at least one clause is 'free',
		#then the KB is not currently satisfied by the model (yet):
		if flag_clause == 'free':
			flag_KB = 'free'

	#If we did not encounter any 'false' or 'free' clauses in the KB,
	#then all clauses are 'true' and the KB is satisfied. Hence the model
	#satisfies the KB:
	if flag_KB == 'true':
		return True, model


	#If we reached this point, it means that
	#the model does not currently satisfy the KB (yet).

	#Invoking the pure symbol heuristic:

	signs_dict = findPureSymbol(KB, model)
	list_of_pure_symbols = [i for i in signs_dict if signs_dict[i]!=None]

	#If the list of pure symbols is long, we choose to
	#assign a truth value to the symbol that has the highest degree:
	if len(list_of_pure_symbols) > 1:

		#Creating a dictionary with the pure symbols as keys
		#and their degrees as values:
		degrees_of_pure_symbols = {}
		for i in list_of_pure_symbols:
			degrees_of_pure_symbols[i] = degrees[i]

		#Sorting the list of pure symbols by the degrees:
		list_of_pure_symbols = sorted(degrees_of_pure_symbols, key=degrees_of_pure_symbols.get, reverse = True)

	#If the list of pure symbols is nonempty,
	#assign a truth value to the first such symbol:
	if len(list_of_pure_symbols)!=0:
		pureSymbol = list_of_pure_symbols[0]
		del degrees[pureSymbol]
		if signs_dict[pureSymbol] == True:
			model[pureSymbol] = 'true'    #Assign 'true' if the literals are positive
		else:
			model[pureSymbol] = 'false'    #Assign 'false' if the literals are negative
		return DPLL(KB, model, degrees)    #Recursively call DPLL with the new model

	#Invoking the unit clause heuristic:

	unitLiteral = findUnitClause(KB, model)

	#If there exists a unit clause, assign a truth value
	#to the symbol of the literal in that clause:
	if unitLiteral != -1:
		del degrees[unitLiteral.get_name()]
		if unitLiteral.get_sign() == True:
			model[unitLiteral.get_name()] = 'true'    #Assign 'true' if the literal is positive
		else:
			model[unitLiteral.get_name()] = 'false'    #Assign 'false' if the literal is negative
		return DPLL(KB, model, degrees)    #Recursively call DPLL with the new model

	#If none of the two heuristics work, we need to select a symbol and branch it:

	#We first order the symbols based on their degree,
	#so we can branch out the one with maximum degree first:
	ordered_keys = sorted(degrees, key=degrees.get, reverse = True)

	for symbol in ordered_keys:
		model1 = model.copy()
		model2 = model.copy()
		degrees1 = degrees.copy()
		degrees2 = degrees.copy()

		#Assigning the symbol to 'true':
		model1[symbol] = "true"
		del degrees1[symbol]

		satisfiable1, model1 = DPLL(KB, model1, degrees1)    #Recursively call DPLL with the new model

		if satisfiable1 == True:
			#We found a model that satisfies the KB for the 'true' assignment.
			return True, model1

		#Assigning the symbol to 'false':
		model2[symbol] = "false"
		del degrees2[symbol]

		satisfiable2, model2 = DPLL(KB, model2, degrees2)    #Recursively call DPLL with the new model

		if satisfiable2 == True:
			#We found a model that satisfies the KB for the 'false' assignment.
			return True, model2

		else:
			#Both values for the symbol failed to give a model that satisfies the KB.
			#Hence the KB is unsatisfiable.
			return False, {}

#Defining the literals:
A = Literal("A")
B = Literal("B")
C = Literal("C")
D = Literal("D")
E = Literal("E")
F = Literal("F")

#Defining the KBs:
KB1 = [{A,B},{A,-C},{-A,B,D}]
KB2 = [{-A,B,E},{-B,A},{-E,A},{D,-E},{-B,-C,-F},{-E,B},{-B,F},{-B,C}]

#Printing the results:
print "----"

(satisfiable, model) = DPLLSatisfiable(KB1)
print "Satisfiable:", satisfiable
print "Model:", model

print "----"

(satisfiable, model) = DPLLSatisfiable(KB2)
print "Satisfiable:", satisfiable
print "Model:", model

print "----"
