from matplotlib import pyplot as plt
import networkx as nx
import random
import numpy as np
import math
np.random.seed(0)

class Package:
    def __init__(self, origin_index, destination_index, current_position):
        self.destination_index = destination_index
        self.origin_index = origin_index
        self.current_position = origin_index

    def set_destination(self, destination_index):
        self.destination_index = destination_index

    def get_destination(self):
        return self.destination_index

    def set_origin(self, origin_index):
        self.origin_index = origin_index

    def get_origin(self):
        return self.origin_index

    def set_current_position(self, current_position):
        self.current_position = current_position

    def get_current_position(self):
        return self.current_position

class Delivery_Network:

    def __init__(self, network_size=10, max_capacity = 100, m = 3, max_distance = 60, max_packages = 20, saturation = 0.4, time = 0, active_nodes_list = [], active_edges_list_small_large = [], active_edges_list_large_small = [], delivered = 0, total_num_packages = 0, viz_pack = []):
        self.network_size = network_size
        self.max_capacity = max_capacity
        self.max_distance = max_distance
        self.m = m
        self.max_packages = max_packages
        self.saturation = saturation
        self.time = time
        self.active_edges_list_small_large = active_edges_list_small_large
        self.active_edges_list_large_small = active_edges_list_large_small
        self.active_nodes_list = active_nodes_list
        self.delivered = delivered
        self.total_num_packages = total_num_packages
        self.viz_pack = viz_pack

    def get_delivered(self):
        return self.delivered

    def get_total(self):
        return self.total_num_packages

    def get_time(self):
        return self.time

    def initialize(self):
        self.graph = nx.barabasi_albert_graph(self.network_size, self.m)
        edges = self.graph.edges
        nodes = self.graph.nodes
        nodes_list = list(self.graph.nodes)
        edges_list = list(self.graph.edges)
        self.active_nodes_list = [i for i in nodes_list]
        self.active_edges_list_small_large = [i for i in edges_list]
        self.active_edges_list_large_small = [(i[1],i[0]) for i in edges_list]

        def remove_node(nodes_list, to_remove):
            copy_nodes_list = [i for i in nodes_list]
            copy_nodes_list.remove(to_remove)
            return copy_nodes_list

        for edge in edges:
            self.graph.edges[edge]['max_capacity_small_large'] = np.random.randint(5,self.max_capacity)
            self.graph.edges[edge]['max_capacity_large_small'] = np.random.randint(5,self.max_capacity)
            self.graph.edges[edge]['current_capacity_small_large'] = 0
            self.graph.edges[edge]['current_capacity_large_small'] = 0
            self.graph.edges[edge]['distance'] = np.random.randint(1,self.max_distance)
            self.graph.edges[edge]['packages_small_large'] = []
            self.graph.edges[edge]['packages_large_small'] = []
        for node in nodes:
            self.graph.nodes[node]['max_num_packages'] = np.random.randint(1,self.max_packages)
        for node in nodes:
            self.graph.nodes[node]['packages'] = []
            modified_nodes = remove_node(nodes_list, node)
            for package_index in range(int(self.graph.nodes[node]['max_num_packages']*self.saturation)):
                current_package = Package(node, np.random.choice(modified_nodes),0)
                self.graph.nodes[node]['packages'].append(current_package)
        self.total_num_packages = sum(len(self.graph.nodes[node]['packages']) for node in nodes_list)
        print "Total number of packages:", self.total_num_packages
        self.layout = nx.spring_layout(self.graph)

    def update(self):

        self.time += 1
        edges = self.graph.edges
        nodes = self.graph.nodes
        nodes_list = list(self.graph.nodes)
        edges_list = list(self.graph.edges)

        def find_shortest_path(node1, node2, number):
            p=list(nx.shortest_simple_paths(self.graph, node1, node2, weight = 'distance'))
            return p[number], len(p)
        
        def send_package_from_city(package):
            if package.destination_index != package.current_position:
                count = 0
                while True:
                    try_path = find_shortest_path(package.current_position, package.destination_index,count)[0]
                    success = True
                    for i in range(len(try_path)-1):
                        if try_path[i] > try_path[i+1]:
                            if (try_path[i],try_path[i+1]) not in self.active_edges_list_large_small:
                                success = False
                        if try_path[i] < try_path[i+1]:
                            if (try_path[i],try_path[i+1]) not in self.active_edges_list_small_large:
                                success = False
                    if success == True:
                        break
                    count += 1
                    if count>= find_shortest_path(package.current_position, package.destination_index,count-1)[1]:
                        break
                if success==False:
                    print "Could not send package from", package.current_position, "to", package.destination_index
                else:
                    package.set_current_position((try_path[0],try_path[1],0))

                    if try_path[0]>try_path[1] and self.graph.edges[(try_path[1], try_path[0])]['current_capacity_large_small']==self.graph.edges[(try_path[1], try_path[0])]['max_capacity_large_small']-1:
                        self.graph.edges[(try_path[1], try_path[0])]['current_capacity_large_small'] += 1
                        self.active_edges_list_large_small.remove((try_path[0], try_path[1]))
                        self.graph.edges[(try_path[1], try_path[0])]['packages_large_small'].append(package)
                    elif try_path[0]<try_path[1] and self.graph.edges[(try_path[0], try_path[1])]['current_capacity_small_large']==self.graph.edges[(try_path[0], try_path[1])]['max_capacity_small_large']-1:
                        self.graph.edges[(try_path[0], try_path[1])]['current_capacity_small_large'] += 1
                        self.active_edges_list_small_large.remove((try_path[0], try_path[1]))
                        self.graph.edges[(try_path[0], try_path[1])]['packages_small_large'].append(package)
                    elif try_path[0]>try_path[1]:
                        self.graph.edges[(try_path[1], try_path[0])]['current_capacity_large_small'] += 1
                        self.graph.edges[(try_path[1], try_path[0])]['packages_large_small'].append(package)
                    else:
                        self.graph.edges[(try_path[0], try_path[1])]['current_capacity_small_large'] += 1
                        self.graph.edges[(try_path[0], try_path[1])]['packages_small_large'].append(package)
                    if try_path[0] not in self.active_nodes_list:
                        self.active_nodes_list.append(try_path[0])
                    self.graph.nodes[try_path[0]]['packages'].remove(package)



        def receive_package_from_road(package):
            if package.current_position[2] != self.graph.edges[(package.current_position[0],package.current_position[1])]['distance']-1:
                print "ERROR RECEIVING PACKAGE"
            else:
                if package.current_position[1] in self.active_nodes_list:
                    self.graph.nodes[package.current_position[1]]['packages'].append(package)

                    if len(self.graph.nodes[package.current_position[1]]['packages']) == self.graph.nodes[package.current_position[1]]['max_num_packages']:
                        self.active_nodes_list.remove(package.current_position[1])

                    if package.current_position[0]>package.current_position[1]:
                        self.graph.edges[(package.current_position[1], package.current_position[0])]['current_capacity_large_small'] -= 1
                        self.graph.edges[(package.current_position[1], package.current_position[0])]['packages_large_small'].remove(package)
                    if package.current_position[0]<package.current_position[1]:
                        self.graph.edges[(package.current_position[0], package.current_position[1])]['current_capacity_small_large'] -= 1
                        self.graph.edges[(package.current_position[0], package.current_position[1])]['packages_small_large'].remove(package)

                    package.set_current_position(package.current_position[1])
                else:
                    print "Package", package.current_position, "waiting to enter!" 

        def travel(package):
            package.set_current_position((package.current_position[0],package.current_position[1],package.current_position[2]+1))


        for an_edge in edges_list:
            for package in self.graph.edges[an_edge]['packages_small_large']:
                if package.current_position[2] < self.graph.edges[(package.current_position[0],package.current_position[1])]['distance']-1:
                    travel(package)
                else:
                    receive_package_from_road(package)
                    if package.destination_index == package.current_position:
                        self.delivered+=1
                        self.graph.nodes[package.current_position]['packages'].remove(package)
            for package in self.graph.edges[an_edge]['packages_large_small']:
                if package.current_position[2] < self.graph.edges[(package.current_position[0],package.current_position[1])]['distance']-1:
                    travel(package)
                else:
                    receive_package_from_road(package)
                    if package.destination_index == package.current_position:
                        self.delivered+=1
                        self.graph.nodes[package.current_position]['packages'].remove(package)
        self.viz_pack=[]
        for a_node in nodes_list:
            self.viz_pack.append(len(self.graph.nodes[a_node]['packages']))
        for a_node in nodes_list:
            for package in self.graph.nodes[a_node]['packages']:
                send_package_from_city(package)
        print "Delivered packages:", self.delivered



    def observe(self):
        plt.clf()
        nx.draw(
            self.graph, pos=self.layout, with_labels=False,
            node_color=[5*self.viz_pack[i]/float(self.total_num_packages) for i in self.graph.nodes],
            edge_color=[5*(len(self.graph.edges[i, j]['packages_large_small'])+len(self.graph.edges[i, j]['packages_small_large']))/float(self.total_num_packages) for i, j in self.graph.edges],
            edge_cmap=plt.cm.binary, edge_vmin=0., edge_vmax=1., alpha=0.7, vmin=0., vmax=1.)
        plt.title('Road Network')
        plt.show()

    def observe_init(self):
        plt.clf()
        print [len(self.graph.nodes[i]['packages'])/float(self.total_num_packages) for i in self.graph.nodes]
        print [(len(self.graph.edges[i, j]['packages_large_small'])+len(self.graph.edges[i, j]['packages_small_large']))/float(self.total_num_packages) for i, j in self.graph.edges]
        print "---"
        nx.draw(
            self.graph, pos=self.layout, with_labels=False,
            node_color=[5*len(self.graph.nodes[i]['packages'])/float(self.total_num_packages) for i in self.graph.nodes],
            edge_color=[5*(len(self.graph.edges[i, j]['packages_large_small'])+len(self.graph.edges[i, j]['packages_small_large']))/float(self.total_num_packages) for i, j in self.graph.edges],
            edge_cmap=plt.cm.binary, edge_vmin=0., edge_vmax=1., alpha=0.7, vmin=0., vmax=1.)
        plt.title('Road Network')
        plt.show()


sim = Delivery_Network()
sim.initialize()

plt.figure()
sim.observe_init()
for i in range(10000):
    if sim.get_total()==sim.get_delivered():
        print "SUCCESS in", sim.get_time(), "steps"
        break
    sim.update()
    if i%3==2:
        plt.figure()
        sim.observe()
