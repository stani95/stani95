#!/usr/bin/env python
# coding: utf_8

from cyrillic import cyrillicWord
from big_ol_pile_of_manim_imports import *
import random


# To watch one of these scenes, run the following:
# python extract_scene.py file_name <SceneName> -p
# 
# Use the flat -l for a faster rendering at a lower 
# quality, use -s to skip to the end and just show
# the final frame, and use -n <number> to skip ahead
# to the n'th animation of a scene.


class new18(GraphScene):

    CONFIG = {
        "x_min" : -6,
        "x_max" : 6,
        "x_axis_width" : FRAME_WIDTH,
        "x_labeled_nums" : range(-5, 6),
        "y_min" : 0,
        "y_max" : 0.6,
        "y_axis_height" : FRAME_HEIGHT,
        "y_tick_frequency" : 0.1,
        "y_labeled_nums" : [0.5],
        "graph_origin" : ORIGIN+3.2*DOWN,
        "dx" : 0.2,
        "deriv_x_min" : -3,
        "deriv_x_max" : 3,
        "exclude_zero_label": False,
    }

    def construct(self):

        def transform_coords(point):
            x_coord = point[0]
            y_coord = point[1]
            new_x_coord = x_coord*(FRAME_WIDTH/12.)
            new_y_coord = y_coord*(FRAME_HEIGHT/0.6)-3.2
            return np.array([new_x_coord,new_y_coord,0.])

        def transform_vectors(point):
            x_coord = point[0]
            y_coord = point[1]
            new_x_coord = x_coord*(FRAME_WIDTH/12.)
            new_y_coord = y_coord*(FRAME_HEIGHT/0.6)
            return np.array([new_x_coord,new_y_coord,0.])

        def transform_vectors_back(point):
            x_coord = point[0]
            y_coord = point[1]
            new_x_coord = x_coord/(FRAME_WIDTH/12.)
            new_y_coord = y_coord/(FRAME_HEIGHT/0.6)
            return np.array([new_x_coord,new_y_coord,0.])

        def transform_coords_back(point):
            x_coord = point[0]
            y_coord = point[1]
            new_x_coord = x_coord/(FRAME_WIDTH/12.)
            new_y_coord = (y_coord+3.2)/(FRAME_HEIGHT/0.6)
            return np.array([new_x_coord,new_y_coord,0.])

        def count_samples_in_rect(samples, my_rectangle):
            r_w = my_rectangle.get_width()
            r_h = my_rectangle.get_height()
            r_c = my_rectangle.get_center()
            transformed_w_h = transform_vectors_back(np.array([r_w,r_h,0.]))
            transformed_c = transform_coords_back(r_c)

            number = 0
            indices = []
            for i in range(len(samples)):
                if transform_coords_back(samples[i].get_center())[0]<transformed_c[0]+transformed_w_h[0]/2. and transform_coords_back(samples[i].get_center())[0]>transformed_c[0]-transformed_w_h[0]/2. and transform_coords_back(samples[i].get_center())[1]>transformed_c[1]-transformed_w_h[1]/2. and transform_coords_back(samples[i].get_center())[1]<transformed_c[1]+transformed_w_h[1]/2.:
                    number+=1
                    indices.append(i)
            return number, indices

        self.setup_axes(animate = False)
        mu = 1.
        sigma = 1.
        def f(x):
            return (1./math.sqrt(2*math.pi*sigma**2))*math.exp(-((x-mu)**2)/(2*sigma**2))
        graph = self.get_graph(lambda x : f(x))
        color_kwargs = {
            "fill_color" : GREEN,
            "fill_opacity" : 0.2,
            "stroke_color" : BLACK,            
            "stroke_width" : 0.3,
        }
        #To get a segment of length 1 in graph space,
        #construct a segment of length 1 in normal space
        #and scale it by (FRAME_WIDTH/12.) (for x),
        #or by (FRAME_HEIGHT/0.6) (for y).
        width_true = 1.2
        height_true = 0.06
        width = width_true*(FRAME_WIDTH/12.)
        height = height_true*(FRAME_HEIGHT/0.6)
        r1 = Rectangle(
            width = width,
            height = height,
            **color_kwargs
        )
        r1.shift(transform_vectors(np.array([ 2., -0.24+0.1, 0.])))
        r2 = Rectangle(
            width = width,
            height = height,
            **color_kwargs
        )
        r2.shift(transform_vectors(np.array([ 0.5, -0.24+0.05, 0.])))

        kwargs = {
            "dx" : self.dx,
            "x_min" : -3.,
            "x_max" : 5.,
            "fill_opacity" : 0.8,
        }
        thin_kwargs = dict(kwargs)
        thin_kwargs["dx"] = 0.002
        thin_kwargs["stroke_width"] = 0
        thin_rects = self.get_riemann_rectangles(
            graph,
            start_color=YELLOW_E,
            end_color=YELLOW_E,
            **thin_kwargs
        )
        samples = []
        samples2 = []
        num_samples = 300

        for i in range(num_samples):
            b = np.random.normal(mu,sigma)
            c = f(b)*random.random()
            samples.append(Dot(transform_coords(np.array([ b,  c, 0.]))))
            samples[i].set_color(RED)
            samples[i].scale(0.65)
            samples2.append(Dot(transform_coords(np.array([ b,  c, 0.]))))
            samples2[i].set_color(GREEN_E)
            samples2[i].scale(1.5)
            if i==0:
                sample0 = TexMobject("%f" % (b), color=WHITE)
                sample0.shift(np.array([-4.,1.5,0.]))
            if i==1:
                sample1 = TexMobject("%f" % (b), color=WHITE)
                sample1.shift(np.array([-4.,2.2,0.]))
                dotdotdot = TextMobject("\\dots")
                dotdotdot.rotate(np.pi/2.)
                dotdotdot.shift(np.array([-4.,0.6,0.]))

        bad_samples = []
        show_bad_samples = []
        hide_bad_samples = []
        tt = 0
        while tt<num_samples:
            b1 = np.random.normal(0.5,0.6)
            b2 = np.random.normal(0.2,0.05)
            if f(b1)>b2 and b2>0:
                bad_samples.append(Dot(transform_coords(np.array([ b1,  b2, 0.]))))
                bad_samples[tt].set_color(GREEN_E)
                bad_samples[tt].scale(0.65)
                show_bad_samples.append(FadeIn(bad_samples[tt]))
                hide_bad_samples.append(FadeOut(bad_samples[tt]))
                tt+=1



        Text_num_samples = TexMobject("Number of points in the rectangle: ", color=WHITE)
        Text_num_samples.scale(0.5)
        Text_num_samples.shift(np.array([3.6,3.,0.]))

        Text_final_samples = TexMobject("Samples from the distribution: ", color=WHITE)
        Text_final_samples.scale(0.6)
        Text_final_samples.shift(np.array([-4,2.8,0.]))

        Text_num_samples_list = []
        Text_num_samples_list_a = []
        Rectangles_list = []

        arrow = Vector(4*RIGHT+3*DOWN, color = BLUE_E)
        arrow.shift(np.array([-2.9,-0.2,0.]))
        arrow2 = Vector(1.5*RIGHT+3*DOWN, color = BLUE_E)
        arrow2.shift(np.array([-2.9,-0.2,0.]))
        arrow3 = Vector(6.4*RIGHT+3*DOWN, color = BLUE_E)
        arrow3.shift(np.array([-2.9,-0.2,0.]))

        Text_num_samples_number = 5

        t=0
        samples_BLACK = []
        while t<Text_num_samples_number:
            b = np.random.normal(mu,sigma)
            text_sample = np.array([ b,  f(b)*random.random(), 0.])
            if t==0:
                old_text_sample = np.array([10.,10.,0.])
            transformed_w_h = transform_vectors_back(np.array([width_true,height_true,0.]))
            ur_corner = text_sample + np.array([width_true/2.,height_true/2.,0.])
            ul_corner = text_sample + np.array([(-1)*width_true/2.,height_true/2.,0.])
            bl_corner = text_sample + np.array([(-1)*width_true/2.,(-1)*height_true/2.,0.])
            if ur_corner[1] < f(ul_corner[0]) and ul_corner[1] < f(ur_corner[0]) and bl_corner[1] > 0. and abs(old_text_sample[0]-text_sample[0])>0.45 and abs(old_text_sample[1]-text_sample[1])>0.045:
                Rectangles_list.append(Rectangle(width = width, height = height, **color_kwargs))
                Rectangles_list[t].shift(transform_vectors(text_sample + np.array([ 0., -0.24, 0.])))
                #print count_samples_in_rect(samples,Rectangles_list[t])
                samples_BLACK.append(count_samples_in_rect(samples,Rectangles_list[t])[1])
                Text_num_samples_list.append(TexMobject("%d" % (count_samples_in_rect(samples,Rectangles_list[t])[0]), color=WHITE))
                Text_num_samples_list[t].scale(0.55)
                Text_num_samples_list[t].shift(Rectangles_list[t].get_center())
                Text_num_samples_list_a.append(TexMobject("%d" % (count_samples_in_rect(samples,Rectangles_list[t])[0]), color=WHITE))
                Text_num_samples_list_a[t].scale(0.55)
                Text_num_samples_list_a[t].shift(np.array([6.6,3.-0.4*t,0.]))
                t+=1
                old_text_sample = text_sample

        samples_BLACK_sets = []
        for i in range(len(samples_BLACK)):
            samples_BLACK_sets.append([])
            for j in samples_BLACK[i]:
                samples_BLACK_sets[i].append(copy.copy(samples[j]))
            for j in samples_BLACK_sets[i]:
                j.set_color(BLACK)



        surround = Rectangle(color = "WHITE", height = 2., width = 0.6, stroke_width = 0.7)
        surround.shift(np.array([6.6,2.2,0.]))



        self.wait(7.)
        self.play(ShowCreation(graph), run_time=3.)
        self.wait(4.)
        self.play(ShowCreation(thin_rects), run_time=4.)
        self.wait(6.)
        self.play(*show_bad_samples, run_time=3.)
        self.wait(10.)
        self.play(*hide_bad_samples, run_time=3.)
        self.wait(0.5)
        for i in range(num_samples):
            self.play(ShowCreation(samples[i]), run_time=0.01)
        self.wait(10.)

        samples_x = []
        samples_y = []
        show_samples_y = []
        for i in range(num_samples):
            samples_x.append(Dot(np.array([samples[i].get_center()[0],-3.2,0.])))
            samples_x[i].set_color(GREEN_E)
            samples_x[i].scale(0.65)
            samples_y.append(Dot(np.array([samples[i].get_center()[0],-3.2,0.])))
            samples_y[i].set_color(GREEN_E)
            samples_y[i].scale(0.65)
            if i!=0 and i!=1:
                show_samples_y.append(ShowCreation(samples_y[i]))


        for i in range(Text_num_samples_number):
            if i==0:
                self.play(ShowCreation(Rectangles_list[i]))
                self.wait(5.)
                self.play(Write(Text_num_samples), run_time=2.)
                self.wait(5.)
            else:
                self.play(ReplacementTransform(Rectangles_list[i-1],Rectangles_list[i]))
            self.wait(2.)
            black_to_number = []
            for j in samples_BLACK_sets[i]:
                self.play(ShowCreation(j), run_time=0.1)
                black_to_number.append(ReplacementTransform(j, Text_num_samples_list[i])) 
            if len(black_to_number)>0:
                self.play(*black_to_number, run_time=3.)
            self.wait(2.)
            self.play(ReplacementTransform(Text_num_samples_list[i], Text_num_samples_list_a[i]), run_time=2.)
            if i==Text_num_samples_number-1:
                self.play(FadeOut(Rectangles_list[i]))
            self.wait(2.)
        self.play(ShowCreation(surround), run_time = 2.)
        self.wait(4)
        self.play(FadeOut(surround), FadeOut(Text_num_samples_list_a[0]), FadeOut(Text_num_samples_list_a[1]), FadeOut(Text_num_samples_list_a[2]), FadeOut(Text_num_samples_list_a[3]), FadeOut(Text_num_samples_list_a[4]), FadeOut(Text_num_samples), run_time = 1.5)

        '''
        for i in range(num_samples):
            self.play(ReplacementTransform(samples[i], samples2[i]), run_time=3./(1.+i**1.05))
            self.play(ReplacementTransform(samples2[i], samples_x[i]), run_time=3./(1.+i**1.05))
        '''
        transforms = []
        for i in range(2,num_samples):
            transforms.append(ReplacementTransform(samples[i],samples_x[i]))
        transforms2 = []
        for i in range(2,num_samples):
            transforms2.append(ReplacementTransform(samples_x[i],dotdotdot))
        self.wait(4.)
        self.play(Write(Text_final_samples), run_time=2.)
        self.play(ReplacementTransform(samples[1], samples2[1]), run_time=3.)
        self.wait(2.)
        self.play(ReplacementTransform(samples2[1], samples_x[1]), run_time=3.)
        self.play(ShowCreation(samples_y[1]), run_time=0.5)
        self.wait(1.5)
        self.play(ReplacementTransform(samples_x[1], sample1), run_time=3.)
        self.wait(4.)
        self.play(ReplacementTransform(samples[0], samples2[0]), run_time=3.)
        self.play(ReplacementTransform(samples2[0], samples_x[0]), run_time=3.)
        self.play(ShowCreation(samples_y[0]), run_time=0.5)
        self.play(ReplacementTransform(samples_x[0], sample0), run_time=3.)
        self.wait(2.)
        self.play(*transforms, run_time=6.)
        self.play(*show_samples_y, run_time=0.5)
        self.play(*transforms2, run_time=2.5)
        self.wait(15.)
        self.play(ShowCreation(arrow))
        self.wait(5.)
        self.play(ReplacementTransform(arrow,arrow2), run_time=1.5)
        self.wait(5.)
        self.play(ReplacementTransform(arrow2,arrow3), run_time=1.5)

        self.wait(5.)
