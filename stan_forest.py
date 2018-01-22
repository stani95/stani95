import matplotlib
matplotlib.use('TkAgg')
import pylab
import matplotlib.pyplot as plt
#pylab.seed(0)

class Forest(object):
    def __init__(self, n = 100, init_p = 0.85, bound_cond = "periodic"):
        self.n = n
        self.init_p = init_p
        self.bound_cond = bound_cond
        self.state = pylab.zeros([self.n, self.n])
        self.next_state = pylab.zeros([self.n, self.n])
        self.time = 0.0
        self.burned_area_list = []
        self.burned_area = 0.0
        self.total_num_trees = 0.0
        self.total_burned_area = 0.0

    #Set and get methods:
    def set_n(self,n):
        self.n=n
    def set_p(self,init_p):
        self.init_p=init_p
    def set_state(self,state):
        self.state=state
    def set_next_state(self,next_state):
        self.next_state=next_state
    def get_n(self):
        return self.n
    def get_p(self):
        return self.init_p
    def get_state(self):
        return self.state
    def get_next_state(self):
        return self.next_state
    def get_time(self):
    	return self.time
    def get_total_burned_area(self):
    	return self.total_burned_area

    def initialize(self):
        self.state = pylab.zeros([self.n, self.n])
        for x in xrange(self.n):
            for y in xrange(self.n):
                self.state[x, y] = 1 if pylab.random() < self.init_p else 0
        self.state[self.n/2, self.n/2] = 2
        self.next_state = pylab.zeros([self.n, self.n])
        for x in xrange(self.n):
            for y in xrange(self.n):
            	if self.state[x, y] == 1 or self.state[x, y] == 2:
            		self.total_num_trees += 1
        #self.density_history = [self.config.mean()]

    def observe(self):
        pylab.cla()
        pylab.subplot(1, 2, 1)
        pylab.pcolor(self.state, vmin = 0, vmax = 3, cmap = pylab.cm.binary)
        pylab.axis('image')
        #pylab.title('t = ' + str(time))
        pylab.subplot(1, 2, 2)
        pylab.plot(self.burned_area_list)
        pylab.ylim(0, 1)

    def update(self):
    	stopped = True
        for x in xrange(self.n):
            for y in xrange(self.n):
            	if self.state[x, y] == 2:
            		self.burned_area += 1
            		stopped = False
            		self.next_state[x,y] = 3
            	elif self.state[x, y] == 1:
            		self.next_state[x, y] = 1
            		for dx in [-1,0,1]:
            			for dy in [-1,0,1]:
            				if self.state[ (x + dx) % self.n, (y + dy) % self.n ] == 2:
            					self.next_state[x, y] = 2
            	else:
            		self.next_state[x, y] = self.state[x, y]
        self.state, self.next_state = self.next_state, self.state
        self.burned_area_list.append(self.burned_area/float(self.total_num_trees))
        if stopped == False:
        	self.time += 1
        if stopped == True:
        	self.total_burned_area = self.burned_area/float(self.total_num_trees)



my_forest = Forest()
import pycxsimulator
pycxsimulator.GUI().start(func=[my_forest.initialize, my_forest.observe,my_forest.update])

my_forests = [[Forest(100, 0.05+0.05*i, "periodic") for j in range(5)] for i in range(20)]

all_avg_times = []
all_avg_burned_areas = []
k=0
for group_same_density in my_forests:
	avg_time = 0
	avg_burned_area = 0
	for one_forest in group_same_density:
		k+=1
		print "doing forest", k
		one_forest.initialize()
		prev_time = 0
		while one_forest.get_time() != prev_time or prev_time == 0:
			prev_time = one_forest.get_time()
			one_forest.update()
		avg_time += prev_time
		avg_burned_area += one_forest.get_total_burned_area()
	all_avg_burned_areas.append(avg_burned_area/5.0)
	all_avg_times.append(avg_time/5.0)

plt.subplot(1, 2, 1)
plt.plot([0.05+0.05*i for i in range(20)], all_avg_times)
plt.title("Time it takes for fire to stop spreading")
plt.subplot(1, 2, 2)
plt.plot([0.05+0.05*i for i in range(20)], all_avg_burned_areas)
plt.title("Fraction of area burned")
plt.ylim(0, 1)
plt.show()
