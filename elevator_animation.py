#!/usr/bin/env python
# coding: utf_8

import random
import numpy as np
random.seed(0)
np.random.seed(0)
import math

from cyrillic import cyrillicWord

from mobject.tex_mobject import *
from mobject import *
from mobject.image_mobject import *
from mobject.vectorized_mobject import *
from mobject.point_cloud_mobject import *
from mobject.region import *
from mobject.svg_mobject import *

from animation.animation import *
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *

from topics.geometry import *
from topics.complex_numbers import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from topics.arithmetic import *
from topics.fractals import *
from topics.graph_theory import *
from topics.matrix import *
from topics.numerals import *
from topics.objects import *
from topics.three_dimensions import *
from topics.vector_space_scene import *

from scene import *
#from scene.scene_from_video import *
from scene.test import *
from scene.tk_scene import *
from scene.zoomed_scene import *

from camera import *

from constants import *

from hanoi import *

#from stage_animations.py import *

from helpers import *

from eoc.graph_scene import *

class Elevator(object):

    def __init__(self, max_capacity = 5):
        self.cur_floor = 0.
        self.DOT = "Up"
        self.passengers_in_elevator_list = []
        self.cur_time = 0
        self.max_capacity = max_capacity
        self.happy_people = 0
        self.all_passenger_list = []
        self.queue_list = []
        self.action_time = 0
        self.last_check = 0
        self.top_floor = 0

    def set_cur_time(self, cur_time):
        self.cur_time = cur_time

    def set_all_passenger_list(self, all_passenger_list):
        self.all_passenger_list = all_passenger_list


    def set_passengers_in_elevator_list(self):
        self.passengers_in_elevator_list = [None for i in range(len(self.all_passenger_list))]
        
    def set_top_floor(self, top_floor):
        self.top_floor = top_floor

    def update_time(self):
        return self.action_time

    def get_queue_list(self):
        return self.queue_list

    def move(self, direction):
        if direction == "Up":
            self.cur_floor += 0.25
        else:
            self.cur_floor += -0.25

    def change_direction(self):
        if self.DOT == "Up":
            self.DOT = "Down"
        else:
            self.DOT = "Up"

    def new_passenger(self, new_passengers_list):
        identities_list = [i.identity for i in new_passengers_list]
        identities_list2 = [i.identity for i in new_passengers_list]
        delete_list = []
        counter = 0
        people_who_actually_got_on = []
        while len(new_passengers_list)>counter and len([x for x in self.passengers_in_elevator_list if x is not None]) < self.max_capacity:
            counter += 1
            smallest_id_among_passengers = min(identities_list)
            index_of_smallest_id_among_passengers = identities_list2.index(smallest_id_among_passengers)
            index_of_smallest_id_among_passengers2 = identities_list.index(smallest_id_among_passengers)
            self.passengers_in_elevator_list[smallest_id_among_passengers] = new_passengers_list[index_of_smallest_id_among_passengers]
            people_who_actually_got_on.append(smallest_id_among_passengers)

            delete_list.append(index_of_smallest_id_among_passengers)
            del identities_list[index_of_smallest_id_among_passengers2]
        for i in range(counter-1,-1,-1):
            del new_passengers_list[delete_list[i]]
        indeces_to_delete_from_queue_list = []
        for j in self.queue_list:
            if j[2] in people_who_actually_got_on:
                indeces_to_delete_from_queue_list.append(self.queue_list.index(j))
        for j in range(len(indeces_to_delete_from_queue_list)-1,-1,-1):
            del self.queue_list[indeces_to_delete_from_queue_list[j]]
        if len(new_passengers_list)>0:
            print "Elevator is FULL!!! Some passengers could not enter!"
        return people_who_actually_got_on

    def passenger_exit(self, exit_passengers_list):
        exit_destinations = [i.destination for i in exit_passengers_list]
        if exit_destinations != [self.cur_floor for i in range(len(exit_passengers_list))]:
            print "Warning!!! Some passenger(s) do(es) not want to exit on this floor!!!"
        else:
            for exit_passenger in exit_passengers_list:
                self.passengers_in_elevator_list[exit_passenger.identity] = None
            self.happy_people += len(exit_passengers_list)

    def update_last_check(self):
        self.last_check = self.cur_time

    def simulation(self):
        self.action_time = 0

        for passenger in self.all_passenger_list:
            if passenger.time_appeared > self.last_check and passenger.time_appeared <= self.cur_time:
                self.queue_list.append([passenger.pickup_floor, passenger.direction, passenger.identity])
        self.update_last_check()

        if len(self.queue_list) == 0 and self.passengers_in_elevator_list == [None for i in range(len(self.passengers_in_elevator_list))]:
            return [[], [], self.cur_floor, []]


        elif self.passengers_in_elevator_list == [None for i in range(len(self.passengers_in_elevator_list))]:
            if self.DOT == "Up":
                temp_goal= max(item[0] for item in self.queue_list)
                if temp_goal > self.cur_floor:
                    goal = temp_goal
                elif temp_goal < self.cur_floor:
                    self.change_direction()
                    goal = min(item[0] for item in self.queue_list)
                else :
                    goal = self.cur_floor
            elif self.DOT == "Down":
                temp_goal= min(item[0] for item in self.queue_list)
                if temp_goal < self.cur_floor:
                    goal = temp_goal
                elif temp_goal > self.cur_floor:
                    self.change_direction()
                    goal = max(item[0] for item in self.queue_list)
                else :
                    goal = self.cur_floor

        else :
            if self.DOT == "Up":
                goal = max(passenger.destination for passenger in [i for i in self.passengers_in_elevator_list if i != None])
            else:
                goal = min(passenger.destination for passenger in [i for i in self.passengers_in_elevator_list if i != None])

        if goal > self.cur_floor and self.DOT == "Up":
            self.move("Up")
        elif goal > self.cur_floor and self.DOT == "Down":
            self.DOT = "Up"
            self.move("Up")
        elif goal < self.cur_floor and self.DOT == "Down":
            self.move("Down")
        elif goal < self.cur_floor and self.DOT == "Up":
            self.DOT = "Down"
            self.move("Down")
        elif goal == self.cur_floor:
            self.change_direction()
        getting_off = []
        for i in range(0,len(self.passengers_in_elevator_list)):
            if self.passengers_in_elevator_list[i] != None:
                if self.cur_floor == self.passengers_in_elevator_list[i].destination:
                    getting_off.append(self.passengers_in_elevator_list[i])
                    self.passengers_in_elevator_list[i] = None
                    self.action_time = 4
        self.passenger_exit(getting_off)

        getting_on = []
        for i in range(0,len(self.queue_list)):
            if (self.cur_floor == self.queue_list[i][0] and self.DOT == self.queue_list[i][1]):
                getting_on.append(self.all_passenger_list[self.queue_list[i][2]])
                self.action_time = 4
        who_actually_got_on = self.new_passenger(getting_on)

        if len(getting_off)==0:
            return1 = []
        else:
            return1 = [i.identity for i in getting_off]
        return [who_actually_got_on, return1, self.cur_floor, [i.identity for i in self.passengers_in_elevator_list if i != None]]


    def simulation_2(self):
        self.action_time = 0
        for passenger in self.all_passenger_list:
            if passenger.time_appeared > self.last_check and passenger.time_appeared <= self.cur_time:
                self.queue_list.append([passenger.pickup_floor, passenger.direction, passenger.identity])
        self.update_last_check()
    
        if self.DOT == "Up" and self.cur_floor != self.top_floor:
            self.move("Up")
        elif self.DOT == "Down" and self.cur_floor != 0:
            self.move("Down")
        elif self.DOT == "Up" and self.cur_floor == self.top_floor:
            self.change_direction()
        elif self.DOT == "Down" and self.cur_floor == 0:
            self.change_direction()

        getting_off = []
        for i in range(0,len(self.passengers_in_elevator_list)):
            if self.passengers_in_elevator_list[i] != None:
                if self.cur_floor == self.passengers_in_elevator_list[i].destination:
                    getting_off.append(self.passengers_in_elevator_list[i])
                    self.passengers_in_elevator_list[i] = None
                    self.action_time = 4
        self.passenger_exit(getting_off)

        getting_on = []
        for i in range(0,len(self.queue_list)):
            if (self.cur_floor == self.queue_list[i][0] and self.DOT == self.queue_list[i][1]):
                getting_on.append(self.all_passenger_list[self.queue_list[i][2]])
                self.action_time = 4
        who_actually_got_on = self.new_passenger(getting_on)

        if len(getting_off)==0:
            return1 = []
        else:
            return1 = [i.identity for i in getting_off]
        return [who_actually_got_on, return1, self.cur_floor, [i.identity for i in self.passengers_in_elevator_list if i != None]]

class Passenger(object):
    def __init__(self, time_appeared = 0., destination = 1, pickup_floor = 0, identity = 0):
        self.pickup_floor = pickup_floor
        self.time_appeared = time_appeared
        self.time_exited = 0.
        self.destination = destination
        self.pickup_time = 0.
        self.identity = identity
        self.direction = "Up" if (self.destination-self.pickup_floor) > 0 else "Down"

    def set_time_exited(self, time_exited):
        self.time_exited = time_exited

    def set_pickup_time(self, pickup_time):
        self.pickup_time = pickup_time

    def get_time_appeared(self):
        return self.time_appeared

    def get_destination(self):
        return self.destination


class Building(object):
    def __init__(self, distribution_of_people, total_num_passengers):
        self.distribution_of_people = distribution_of_people
        self.floors = len(distribution_of_people)
        self.total_num_passengers = total_num_passengers
    
    def get_floors(self):
        return self.floors
    
    def get_distribution(self):
        return self.distribution_of_people

    def get_total_num_passengers(self):
        return self.total_num_passengers


class Elevator_Simulation(Scene):
    def construct(self):

        n_fl = input("How many floors does the building have?")

        l=80./float(11*n_fl+1)
        m=8./float(11*n_fl+1)

        x11=[]
        y11=[]
        x12=[]
        y12=[]
        x21=[]
        y21=[]
        x22=[]
        y22=[]

        for i in range(n_fl):
            y11.append(-4+m+i*(m+l))
            x11.append(-float(l)/2)
            y12.append(-4+m+l+i*(m+l))
            x12.append(-float(l)/2)
            y21.append(-4+m+l+i*(m+l))
            x21.append(float(l)/2)
            y22.append(-4+m+i*(m+l))
            x22.append(float(l)/2)

        boxes = []

        for i in range(n_fl):
            boxes.append([Line(np.array([ x11[i],  y11[i],  0.]), np.array([ x12[i],  y12[i],  0.]), color = ORANGE), Line(np.array([ x12[i],  y12[i],  0.]), np.array([ x21[i],  y21[i],  0.]), color = ORANGE), Line(np.array([ x21[i],  y21[i],  0.]), np.array([ x22[i],  y22[i],  0.]), color = ORANGE), Line(np.array([ x22[i],  y22[i],  0.]), np.array([ x11[i],  y11[i],  0.]), color = ORANGE)])
            self.play(ShowCreation(boxes[i][0]), ShowCreation(boxes[i][1]), ShowCreation(boxes[i][2]), ShowCreation(boxes[i][3]), run_time=0.3, submobject_mode = "all_at_once")

        E = TextMobject("E")
        E.move_to(np.array([ -float(l)/2-0.65,  -4+m+0*(m+l)+l/2.,  0.]))
        E.scale_in_place(1.1)
        E.highlight(WHITE)

        Zero = TextMobject("0")
        Zero.move_to(np.array([ -float(l)/2-1.5,  -4+m+0*(m+l)+l/2.,  0.]))
        Zero.scale_in_place(1.1)
        Zero.highlight(WHITE)
        One = TextMobject("1")
        One.move_to(np.array([ -float(l)/2-1.5,  -4+m+1*(m+l)+l/2.,  0.]))
        One.scale_in_place(1.1)
        One.highlight(WHITE)
        Two = TextMobject("2")
        Two.move_to(np.array([ -float(l)/2-1.5,  -4+m+2*(m+l)+l/2.,  0.]))
        Two.scale_in_place(1.1)
        Two.highlight(WHITE)
        Three = TextMobject("3")
        Three.move_to(np.array([ -float(l)/2-1.5,  -4+m+3*(m+l)+l/2.,  0.]))
        Three.scale_in_place(1.1)
        Three.highlight(WHITE)
        Four = TextMobject("4")
        Four.move_to(np.array([ -float(l)/2-1.5,  -4+m+4*(m+l)+l/2.,  0.]))
        Four.scale_in_place(1.1)
        Four.highlight(WHITE)
        Five = TextMobject("5")
        Five.move_to(np.array([ -float(l)/2-1.5,  -4+m+5*(m+l)+l/2.,  0.]))
        Five.scale_in_place(1.1)
        Five.highlight(WHITE)
        Six = TextMobject("6")
        Six.move_to(np.array([ -float(l)/2-1.5,  -4+m+6*(m+l)+l/2.,  0.]))
        Six.scale_in_place(1.1)
        Six.highlight(WHITE)
        Seven = TextMobject("7")
        Seven.move_to(np.array([ -float(l)/2-1.5,  -4+m+7*(m+l)+l/2.,  0.]))
        Seven.scale_in_place(1.1)
        Seven.highlight(WHITE)
        Eight = TextMobject("8")
        Eight.move_to(np.array([ -float(l)/2-1.5,  -4+m+8*(m+l)+l/2.,  0.]))
        Eight.scale_in_place(1.1)
        Eight.highlight(WHITE)
        Nine = TextMobject("9")
        Nine.move_to(np.array([ -float(l)/2-1.5,  -4+m+9*(m+l)+l/2.,  0.]))
        Nine.scale_in_place(1.1)
        Nine.highlight(WHITE)
        Ten = TextMobject("10")
        Ten.move_to(np.array([ -float(l)/2-1.5,  -4+m+10*(m+l)+l/2.,  0.]))
        Ten.scale_in_place(1.1)
        Ten.highlight(WHITE)
        Eleven = TextMobject("11")
        Eleven.move_to(np.array([ -float(l)/2-1.5,  -4+m+11*(m+l)+l/2.,  0.]))
        Eleven.scale_in_place(1.1)
        Eleven.highlight(WHITE)
        self.play(Write(E), run_time=0.5)
        if n_fl==2:
            self.play(ShowCreation(Zero), ShowCreation(One), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==3:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==4:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==5:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==6:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), ShowCreation(Five), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==7:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), ShowCreation(Five), ShowCreation(Six), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==8:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), ShowCreation(Five), ShowCreation(Six), ShowCreation(Seven), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==9:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), ShowCreation(Five), ShowCreation(Six), ShowCreation(Seven), ShowCreation(Eight), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==10:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), ShowCreation(Five), ShowCreation(Six), ShowCreation(Seven), ShowCreation(Eight), ShowCreation(Nine), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==11:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), ShowCreation(Five), ShowCreation(Six), ShowCreation(Seven), ShowCreation(Eight), ShowCreation(Nine), ShowCreation(Ten), run_time=0.5, submobject_mode = "all_at_once")
        if n_fl==12:
            self.play(ShowCreation(Zero), ShowCreation(One), ShowCreation(Two), ShowCreation(Three), ShowCreation(Four), ShowCreation(Five), ShowCreation(Six), ShowCreation(Seven), ShowCreation(Eight), ShowCreation(Nine), ShowCreation(Ten), ShowCreation(Eleven), run_time=0.5, submobject_mode = "all_at_once")

        DotSetUp=[]
        DotSetDown=[]
        for j in range(200):
            NewDots1=[]
            NewDots2=[]
            NewDots3=[]
            LUD = []
            CUD = []
            RUD = []
            LCD = []
            CCD = []
            RCD = []
            LDD = []
            CDD = []
            RDD = []
            for i in range(n_fl):
                NewDots2.append(Dot(np.array([ 8., -4+m+i*(m+l)+l/2., 0.]), color=RED).scale_in_place(1.))
                NewDots3.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2., 0.]), color=GREEN).scale_in_place(1.))
                LUD.append(Dot(np.array([ -l/4., -4+m+i*(m+l)+l/2.+l/4., 0.]), color=RED).scale_in_place(1.))
                CUD.append(Dot(np.array([ 0., -4+m+i*(m+l)+l/2.+l/4., 0.]), color=RED).scale_in_place(1.))
                RUD.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2.+l/4., 0.]), color=RED).scale_in_place(1.))
                LCD.append(Dot(np.array([ -l/4., -4+m+i*(m+l)+l/2., 0.]), color=RED).scale_in_place(1.))
                CCD.append(Dot(np.array([ 0., -4+m+i*(m+l)+l/2., 0.]), color=RED).scale_in_place(1.))
                RCD.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2., 0.]), color=RED).scale_in_place(1.))
                LDD.append(Dot(np.array([ -l/4., -4+m+i*(m+l)+l/2.-l/4., 0.]), color=RED).scale_in_place(1.))
                CDD.append(Dot(np.array([ 0., -4+m+i*(m+l)+l/2.-l/4., 0.]), color=RED).scale_in_place(1.))
                RDD.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2.-l/4., 0.]), color=RED).scale_in_place(1.))
            NewDots1.append(LUD)
            NewDots1.append(CUD)
            NewDots1.append(RUD)
            NewDots1.append(LCD)
            NewDots1.append(CCD)
            NewDots1.append(RCD)
            NewDots1.append(LDD)
            NewDots1.append(CDD)
            NewDots1.append(RDD)

            NewDots1_D=[]
            NewDots2_D=[]
            NewDots3_D=[]
            LUD_D = []
            CUD_D = []
            RUD_D = []
            LCD_D = []
            CCD_D = []
            RCD_D = []
            LDD_D = []
            CDD_D = []
            RDD_D = []
            for i in range(n_fl):
                NewDots2_D.append(Dot(np.array([ 8., -4+m+i*(m+l)+l/2., 0.]), color=BLUE).scale_in_place(1.))
                NewDots3_D.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2., 0.]), color=GREEN).scale_in_place(1.))
                LUD_D.append(Dot(np.array([ -l/4., -4+m+i*(m+l)+l/2.+l/4., 0.]), color=BLUE).scale_in_place(1.))
                CUD_D.append(Dot(np.array([ 0., -4+m+i*(m+l)+l/2.+l/4., 0.]), color=BLUE).scale_in_place(1.))
                RUD_D.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2.+l/4., 0.]), color=BLUE).scale_in_place(1.))
                LCD_D.append(Dot(np.array([ -l/4., -4+m+i*(m+l)+l/2., 0.]), color=BLUE).scale_in_place(1.))
                CCD_D.append(Dot(np.array([ 0., -4+m+i*(m+l)+l/2., 0.]), color=BLUE).scale_in_place(1.))
                RCD_D.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2., 0.]), color=BLUE).scale_in_place(1.))
                LDD_D.append(Dot(np.array([ -l/4., -4+m+i*(m+l)+l/2.-l/4., 0.]), color=BLUE).scale_in_place(1.))
                CDD_D.append(Dot(np.array([ 0., -4+m+i*(m+l)+l/2.-l/4., 0.]), color=BLUE).scale_in_place(1.))
                RDD_D.append(Dot(np.array([ +l/4., -4+m+i*(m+l)+l/2.-l/4., 0.]), color=BLUE).scale_in_place(1.))
            NewDots1_D.append(LUD_D)
            NewDots1_D.append(CUD_D)
            NewDots1_D.append(RUD_D)
            NewDots1_D.append(LCD_D)
            NewDots1_D.append(CCD_D)
            NewDots1_D.append(RCD_D)
            NewDots1_D.append(LDD_D)
            NewDots1_D.append(CDD_D)
            NewDots1_D.append(RDD_D)

            DotSetUp.append([NewDots1,NewDots2,NewDots3])
            DotSetDown.append([NewDots1_D,NewDots2_D,NewDots3_D])

        def new_dot(count,level,count6,destin):
            if destin>level:
                NewDots2 = DotSetUp[count][1]
            else:
                NewDots2 = DotSetDown[count][1]
            self.play(ApplyMethod(NewDots2[level].shift, np.array([ float(l)/2+0.15+count6[level]*0.18-8., 0., 0. ])), run_time=0.8)
            count+=1
            count6[level]+=1
            count6[level] = count6[level]%6
            return count,NewDots2,count6

        def get_in_elevator(count,NewDots2,level,stuffed,count9,up_d):
            if up_d=="up":
                NewDots1 = DotSetUp[count][0][count9]
            elif up_d=="down":
                NewDots1 = DotSetDown[count][0][count9]
            else:
                print "SOMETHING WENT WRONG!!!!!!!!!!!"
            self.play(Transform(NewDots2[level],NewDots1[level]), run_time=0.7)

            stuffed+=1
            count+=1
            count9+=1
            count9=count9%9
            return count,NewDots1[level],stuffed,count9,NewDots2[level]

        def get_out_of_elevator(count,NewDots1,level,stuffed,up_d,is_second):
            if up_d == "up":
                NewDots3 = DotSetUp[count][2]
            elif up_d == "down":
                NewDots3 = DotSetDown[count][2]
            else:
                print "SOMETHING WENT WRONG!!!!!!!!!!"
            if is_second==0:
                self.play(Transform(NewDots1,NewDots3[level]), run_time=0.5)
            else:
                additional_dot = Dot(np.array([ +l/4., -4+m+level*(m+l)+l/2., 0.]), color=GREEN).scale_in_place(1.)
                self.play(Transform(NewDots1,additional_dot), run_time=0.5)
            self.remove(NewDots1)
            if is_second==0:
                self.play(ApplyMethod(NewDots3[level].shift, np.array([ 8., 0., 0. ])), run_time=0.8)
            else:
                self.play(ApplyMethod(additional_dot.shift, np.array([ 8., 0., 0. ])), run_time=0.8)
            stuffed-=1
            count+=1
            return stuffed

        def move_E(E,up_down,Dots):
            if len(Dots)==0:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), run_time=0.7)
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), run_time=0.7)
            elif len(Dots)==1:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
            elif len(Dots)==2:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
            elif len(Dots)==3:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
            elif len(Dots)==4:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
            elif len(Dots)==5:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
            elif len(Dots)==6:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[5].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[5].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
            elif len(Dots)==7:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[5].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[6].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[5].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[6].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
            elif len(Dots)==8:
                if up_down=="up":
                    self.play(ApplyMethod(E.shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[5].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[6].shift, np.array([ 0., m+l, 0. ])), ApplyMethod(Dots[7].shift, np.array([ 0., m+l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")
                else:
                    self.play(ApplyMethod(E.shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[0].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[1].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[2].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[3].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[4].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[5].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[6].shift, np.array([ 0., -m-l, 0. ])), ApplyMethod(Dots[7].shift, np.array([ 0., -m-l, 0. ])), run_time=0.7, submobject_mode = "all_at_once")

###########

        At_Home = Building(distribution_of_people = [60,10,10,10,10,10,10], total_num_passengers = 40)
        num_floors = At_Home.get_floors()
        distribution = At_Home.get_distribution()
        num_passengers = At_Home.get_total_num_passengers()
        distribution = [float(distribution[i])/sum(distribution) for i in range(len(distribution))]

        pickup_locations = np.random.choice(range(num_floors), num_passengers, p=distribution)

        destinations = []
        for i in range(num_passengers):
            distribution_minus_one = [a for a in distribution]
            range_minus_one = range(num_floors)
            del range_minus_one[pickup_locations[i]]
            del distribution_minus_one[pickup_locations[i]]
            distribution_minus_one = [float(distribution_minus_one[i])/sum(distribution_minus_one) for i in range(len(distribution_minus_one))]
            destinations.append(np.random.choice(range_minus_one, 1, p=distribution_minus_one)[0])

        delays = np.random.poisson(lam=120.0, size=num_passengers-1)
        delays = [(i-108)*((i-108)>0) for i in delays]
        times_of_arrival = [3.]
        for i in range(num_passengers-1):
            times_of_arrival.append(times_of_arrival[i]+delays[i])

        passenger_list=[]
        for i in range(num_passengers):
            passenger_list.append(Passenger(time_appeared = times_of_arrival[i], destination = destinations[i], pickup_floor = pickup_locations[i], identity = i))

        cur_time = 0.

        elevator = Elevator()
        elevator.set_all_passenger_list(passenger_list)
        elevator.set_passengers_in_elevator_list()
        elevator.set_top_floor(num_floors-1)
        t_app = [i.time_appeared for i in passenger_list]
        p_fl = [i.pickup_floor for i in passenger_list]
        dest = [i.destination for i in passenger_list]
        ids = [i.identity for i in passenger_list]
        count = 0

        Dots_waiting = []
        Dots_waiting_identity = []
        Dots_boarded = []
        Dots_boarded_identity = []
        Dots_exited = []
        Dots_exited_identity = []

        print "Time appeared:", [i.time_appeared for i in passenger_list]
        print "Pickup floor:", [i.pickup_floor for i in passenger_list]
        print "Destination:", [i.destination for i in passenger_list]
        print "ID:", [i.identity for i in passenger_list]
        c_fl = 0.
        count=0
        stuffed=0
        count9=0
        count6=[0 for i in range(num_floors)]
        while num_passengers!=elevator.happy_people:
            cur_time_old=cur_time
            elevator.set_cur_time(cur_time)
            c_fl_old = c_fl
            all_things = elevator.simulation_2()
            g_on = all_things[0]
            g_off = all_things[1]
            c_fl = all_things[2]
            p_el = all_things[3]
            cur_time+=elevator.update_time()
            cur_time+=0.5
            print "Current time is:", cur_time

            if c_fl_old.is_integer():
                if len(Dots_boarded)==0:
                    if c_fl<c_fl_old:
                        move_E(E,"down",Dots_boarded)
                    elif c_fl==c_fl_old:
                        pass
                    else:
                        move_E(E,"up",Dots_boarded)
                else:
                    if c_fl<c_fl_old:
                        move_E(E,"down",Dots_boarded)
                    elif c_fl==c_fl_old:
                        pass
                    else:
                        move_E(E,"up",Dots_boarded)

            if len(g_off)==0 and len(g_on)!=0:
                self.remove(boxes[int(round(c_fl))][2])
                self.dither(0.1)
            elif len(g_off)==1:
                self.remove(boxes[int(round(c_fl))][2])
                self.dither(0.1)
                up_d="up"
                if p_fl[g_off[0]] > dest[g_off[0]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[0])],int(round(c_fl)),stuffed,up_d,0)
                del Dots_boarded[Dots_boarded_identity.index(g_off[0])]
                del Dots_boarded_identity[Dots_boarded_identity.index(g_off[0])]
            elif len(g_off)==2:
                self.remove(boxes[int(round(c_fl))][2])
                self.dither(0.1)
                up_d="up"
                if p_fl[g_off[0]] > dest[g_off[0]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[0])],int(round(c_fl)),stuffed,up_d,0)
                up_d="up"
                if p_fl[g_off[1]] > dest[g_off[1]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[1])],int(round(c_fl)),stuffed,up_d,1)
                sortedd = sorted(g_off)
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-2])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-2])]
            elif len(g_off)==3:
                self.remove(boxes[int(round(c_fl))][2])
                self.dither(0.1)
                up_d="up"
                if p_fl[g_off[0]] > dest[g_off[0]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[0])],int(round(c_fl)),stuffed,up_d,0)
                up_d="up"
                if p_fl[g_off[1]] > dest[g_off[1]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[1])],int(round(c_fl)),stuffed,up_d,1)
                up_d="up"
                if p_fl[g_off[2]] > dest[g_off[2]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[2])],int(round(c_fl)),stuffed,up_d,1)
                sortedd = sorted(g_off)
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-2])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-2])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-3])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-3])]
            elif len(g_off)==4:
                self.remove(boxes[int(round(c_fl))][2])
                self.dither(0.1)
                up_d="up"
                if p_fl[g_off[0]] > dest[g_off[0]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[0])],int(round(c_fl)),stuffed,up_d,0)
                up_d="up"
                if p_fl[g_off[1]] > dest[g_off[1]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[1])],int(round(c_fl)),stuffed,up_d,1)
                up_d="up"
                if p_fl[g_off[2]] > dest[g_off[2]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[2])],int(round(c_fl)),stuffed,up_d,1)
                up_d="up"
                if p_fl[g_off[3]] > dest[g_off[3]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[3])],int(round(c_fl)),stuffed,up_d,1)
                sortedd = sorted(g_off)
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-2])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-2])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-3])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-3])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-4])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-4])]
            elif len(g_off)==5:
                self.remove(boxes[int(round(c_fl))][2])
                self.dither(0.1)
                up_d="up"
                if p_fl[g_off[0]] > dest[g_off[0]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[0])],int(round(c_fl)),stuffed,up_d,0)
                up_d="up"
                if p_fl[g_off[1]] > dest[g_off[1]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[1])],int(round(c_fl)),stuffed,up_d,1)
                up_d="up"
                if p_fl[g_off[2]] > dest[g_off[2]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[2])],int(round(c_fl)),stuffed,up_d,1)
                up_d="up"
                if p_fl[g_off[3]] > dest[g_off[3]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[3])],int(round(c_fl)),stuffed,up_d,1)
                up_d="up"
                if p_fl[g_off[4]] > dest[g_off[4]]:
                    up_d="down"
                stuffed = get_out_of_elevator(count,Dots_boarded[Dots_boarded_identity.index(g_off[4])],int(round(c_fl)),stuffed,up_d,1)
                sortedd = sorted(g_off)
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-1])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-2])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-2])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-3])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-3])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-4])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-4])]
                del Dots_boarded[Dots_boarded_identity.index(sortedd[-5])]
                del Dots_boarded_identity[Dots_boarded_identity.index(sortedd[-5])]
            elif len(g_off)>5:
                print "!!!"


            if len(g_on)==0 and len(g_off)!=0:
                self.play(ShowCreation(boxes[int(round(c_fl))][2]), run_time = 0.3)
            elif len(g_on)==1:
                up_d="up"
                if int(round(c_fl)) > dest[g_on[0]]:
                    up_d="down"
                count,one_NewDot,stuffed,count9,removee = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[0])],int(round(c_fl)),stuffed,count9,up_d)
                self.play(ShowCreation(boxes[int(round(c_fl))][2]), run_time = 0.3)
                Dots_boarded.append(one_NewDot)
                Dots_boarded_identity.append(g_on[0])
                del Dots_waiting[Dots_waiting_identity.index(g_on[0])]
                del Dots_waiting_identity[Dots_waiting_identity.index(g_on[0])]
            elif len(g_on)==2:
                up_d="up"
                if int(round(c_fl)) > dest[g_on[0]]:
                    up_d="down"
                count,one_NewDot,stuffed,count9,removee1 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[0])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[1]]:
                    up_d="down"
                count,two_NewDot,stuffed,count9,removee2 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[1])],int(round(c_fl)),stuffed,count9,up_d)
                self.play(ShowCreation(boxes[int(round(c_fl))][2]), run_time = 0.3)
                dots_to_get_on=[one_NewDot, two_NewDot]
                sortedd = sorted(g_on)
                sorted_indeces = sorted(range(len(g_on)), key=lambda k: g_on[k])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[0]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[1]])
                Dots_boarded_identity.append(sortedd[0])
                Dots_boarded_identity.append(sortedd[1])
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-2])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-2])]
            elif len(g_on)==3:
                up_d="up"
                if int(round(c_fl)) > dest[g_on[0]]:
                    up_d="down"
                count,one_NewDot,stuffed,count9,removee1 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[0])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[1]]:
                    up_d="down"
                count,two_NewDot,stuffed,count9,removee2 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[1])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[2]]:
                    up_d="down"
                count,three_NewDot,stuffed,count9,removee3 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[2])],int(round(c_fl)),stuffed,count9,up_d)
                self.play(ShowCreation(boxes[int(round(c_fl))][2]), run_time = 0.3)
                dots_to_get_on=[one_NewDot, two_NewDot, three_NewDot]
                sortedd = sorted(g_on)
                sorted_indeces = sorted(range(len(g_on)), key=lambda k: g_on[k])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[0]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[1]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[2]])
                Dots_boarded_identity.append(sortedd[0])
                Dots_boarded_identity.append(sortedd[1])
                Dots_boarded_identity.append(sortedd[2])
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-2])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-2])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-3])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-3])]
            elif len(g_on)==4:
                up_d="up"
                if int(round(c_fl)) > dest[g_on[0]]:
                    up_d="down"
                count,one_NewDot,stuffed,count9,removee1 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[0])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[1]]:
                    up_d="down"
                count,two_NewDot,stuffed,count9,removee2 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[1])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[2]]:
                    up_d="down"
                count,three_NewDot,stuffed,count9,removee3 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[2])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[3]]:
                    up_d="down"
                count,four_NewDot,stuffed,count9,removee4 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[3])],int(round(c_fl)),stuffed,count9,up_d)
                self.play(ShowCreation(boxes[int(round(c_fl))][2]), run_time = 0.3)
                dots_to_get_on=[one_NewDot, two_NewDot, three_NewDot, four_NewDot]
                sortedd = sorted(g_on)
                sorted_indeces = sorted(range(len(g_on)), key=lambda k: g_on[k])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[0]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[1]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[2]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[3]])
                Dots_boarded_identity.append(sortedd[0])
                Dots_boarded_identity.append(sortedd[1])
                Dots_boarded_identity.append(sortedd[2])
                Dots_boarded_identity.append(sortedd[3])
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-2])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-2])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-3])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-3])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-4])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-4])]
            elif len(g_on)==5:
                #self.remove(boxes[int(round(c_fl))][2])
                up_d="up"
                if int(round(c_fl)) > dest[g_on[0]]:
                    up_d="down"
                count,one_NewDot,stuffed,count9,removee1 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[0])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[1]]:
                    up_d="down"
                count,two_NewDot,stuffed,count9,removee2 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[1])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[2]]:
                    up_d="down"
                count,three_NewDot,stuffed,count9,removee3 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[2])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[3]]:
                    up_d="down"
                count,four_NewDot,stuffed,count9,removee4 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[3])],int(round(c_fl)),stuffed,count9,up_d)
                up_d="up"
                if int(round(c_fl)) > dest[g_on[4]]:
                    up_d="down"
                count,five_NewDot,stuffed,count9,removee5 = get_in_elevator(count,Dots_waiting[Dots_waiting_identity.index(g_on[4])],int(round(c_fl)),stuffed,count9,up_d)
                self.play(ShowCreation(boxes[int(round(c_fl))][2]), run_time = 0.3)
                dots_to_get_on=[one_NewDot, two_NewDot, three_NewDot, four_NewDot, five_NewDot]
                sortedd = sorted(g_on)
                sorted_indeces = sorted(range(len(g_on)), key=lambda k: g_on[k])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[0]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[1]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[2]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[3]])
                Dots_boarded.append(dots_to_get_on[sorted_indeces[4]])
                Dots_boarded_identity.append(sortedd[0])
                Dots_boarded_identity.append(sortedd[1])
                Dots_boarded_identity.append(sortedd[2])
                Dots_boarded_identity.append(sortedd[3])
                Dots_boarded_identity.append(sortedd[4])
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-1])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-2])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-2])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-3])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-3])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-4])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-4])]
                del Dots_waiting[Dots_waiting_identity.index(sortedd[-5])]
                del Dots_waiting_identity[Dots_waiting_identity.index(sortedd[-5])]
            elif len(g_on)>5:
                print "!!!"

            jumps = int(round((cur_time - cur_time_old)/0.5))
            times = [cur_time_old+i*0.5 for i in range(1,jumps+1)]
            for j in times:
                if j in t_app:
                    all_indeces = [i for i, x in enumerate(t_app) if x == j]
                    all_pickup_floors = []
                    all_destinations = []
                    for i in all_indeces:
                        all_pickup_floors.append(p_fl[i])
                    for i in all_indeces:
                        all_destinations.append(dest[i])
                    all_identities = []
                    for i in all_indeces:
                        all_identities.append(ids[i])
                    for i in range(len(all_pickup_floors)):
                        count, Newdotttt,count6 = new_dot(count,all_pickup_floors[i],count6,all_destinations[i])
                        Dots_waiting.append(Newdotttt)
                    for j in all_identities:
                        Dots_waiting_identity.append(j)


            self.dither(0.1)
            if len(g_on)==0:
                pass
            elif len(g_on)==1:
                self.remove(removee)
            elif len(g_on)==2:
                self.remove(removee1,removee2)
            elif len(g_on)==3:
                self.remove(removee1,removee2,removee3)
            elif len(g_on)==4:
                self.remove(removee1,removee2,removee3,removee4)
            elif len(g_on)==5:
                self.remove(removee1,removee2,removee3,removee4,removee5)
            else:
                print "!!!"


        self.dither(5.)
