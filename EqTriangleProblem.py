from big_ol_pile_of_manim_imports import *
import random

class EqTriangleProblem(Scene):
    def construct(self):

        title1 = TexMobject("An equilateral triangle", color=BLACK)
        title1.shift(np.array([ 0., 3.3, 0.]))
        title1.scale(0.9)
        title2 = TexMobject("Show that the sum of the", "red", "areas equals the sum of the", "green", "areas", color=BLACK)
        title2.set_color_by_tex("red", RED_E)
        title2.set_color_by_tex("green", GREEN_E)
        title2.shift(np.array([ 0., 3.3, 0.]))
        title2.scale(0.7)

        A0=Dot(np.array([ -2.5,  -3,  0.]), color=BLACK)
        A0.scale(0.5)
        B0=Dot(np.array([ 4,  -3,  0.]), color=BLACK)
        B0.scale(0.5)
        C0=Dot(np.array([ 0.75,  2.63,  0.]), color=BLACK)
        C0.scale(0.5)
        D0=Dot(np.array([ 0.38,  -0.12,  0.]), color=BLACK)
        D0.scale(0.5)
        E0=Dot(np.array([ -0.53,  0.4,  0.]), color=BLACK)
        E0.scale(0.5)
        F0=Dot(np.array([ 1.85,  0.72,  0.]), color=BLACK)
        F0.scale(0.5)
        I0=Dot(np.array([ 0.39,  -3,  0.]), color=BLACK)
        I0.scale(0.5)
        J0=Dot(np.array([ -0.84,  -0.12,  0.]), color=BLACK)
        J0.scale(0.5)
        K0=Dot(np.array([ 2.34,  -0.12,  0.]), color=BLACK)
        K0.scale(0.5)
        L0=Dot(np.array([ 2.34,  -3,  0.]), color=BLACK)
        L0.scale(0.5)
        M0=Dot(np.array([ -0.84,  -3,  0.]), color=BLACK)
        M0.scale(0.5)
        N0=Dot(np.array([ -0.23,  0.93,  0.]), color=BLACK)
        N0.scale(0.5)
        O0=Dot(np.array([ 1.24,  1.78,  0.]), color=BLACK)
        O0.scale(0.5)

        A=np.array([ -2.5,  -3,  0.])
        B=np.array([ 4,  -3,  0.])
        C=np.array([ 0.75,  2.63,  0.])
        D=np.array([ 0.38,  -0.12,  0.])
        E=np.array([ -0.53,  0.4,  0.])
        F=np.array([ 1.85,  0.72,  0.])
        I=np.array([ 0.39,  -3,  0.])
        J=np.array([ -0.84,  -0.12,  0.])
        K=np.array([ 2.34,  -0.12,  0.])
        L=np.array([ 2.34,  -3,  0.])
        M=np.array([ -0.84,  -3,  0.])
        N=np.array([ -0.23,  0.93,  0.])
        O=np.array([ 1.24,  1.78,  0.])

        lineAB = Line( A, B, color = BLACK , stroke_width=0.5)
        lineBC = Line( B, C, color = BLACK , stroke_width=0.5)
        lineCA = Line( C, A, color = BLACK , stroke_width=0.5)
        lineDF = Line( D, F, color = BLACK , stroke_width=0.5)
        lineDI = Line( D, I, color = BLACK , stroke_width=0.5)
        lineDE = Line( D, E, color = BLACK , stroke_width=0.5)
        lineJK = Line( J, K, color = BLACK , stroke_width=0.5)
        lineDO = Line( D, O, color = BLACK , stroke_width=0.5)
        lineDN = Line( D, N, color = BLACK , stroke_width=0.5)
        lineJM = Line( J, M, color = BLACK , stroke_width=0.5)
        lineKL = Line( K, L, color = BLACK , stroke_width=0.5)
        lineNO = Line( N, O, color = BLACK , stroke_width=0.5)
        lineDM = Line( D, M, color = BLACK , stroke_width=0.5)
        lineDA = Line( D, A, color = BLACK , stroke_width=0.5)
        lineDL = Line( D, L, color = BLACK , stroke_width=0.5)
        lineDO = Line( D, O, color = BLACK , stroke_width=0.5)
        lineDC = Line( D, C, color = BLACK , stroke_width=0.5)
        lineDB = Line( D, B, color = BLACK , stroke_width=0.5)
        lineDC = Line( D, C, color = BLACK , stroke_width=0.5)
        poly0=Polygon(C, B, A)
        poly0.set_stroke(color=BLACK, width = 0.)
        poly0.set_fill(color = RED_E, opacity=0.1)
        
        self.play(ShowCreation(lineAB), ShowCreation(lineBC), ShowCreation(lineCA), ShowCreation(A0), ShowCreation(B0), ShowCreation(C0), ShowCreation(poly0), run_time=0.5)
        self.play(ShowCreation(D0), run_time=0.5)
        self.play(ShowCreation(E0), ShowCreation(F0), ShowCreation(I0), ShowCreation(lineDF), ShowCreation(lineDI), ShowCreation(lineDE), run_time=0.5)
        self.wait(0.5)
        self.play(Write(title1))
        self.wait(1.5)
        self.play(*map(FadeOut, [title1]), run_time=0.5)

        poly1=Polygon(D, C, O)
        poly1.set_stroke(color=BLACK, width = 0.)
        poly1.set_fill(color = GREEN_E, opacity=0.9)

        poly1d=Polygon(N, C, O)
        poly1d.set_stroke(color=BLACK, width = 0.)
        poly1d.set_fill(color = GREEN_E, opacity=0.9)

        poly2=Polygon(D, O, F)
        poly2.set_stroke(color=BLACK, width = 0.)
        poly2.set_fill(color = GREEN_E, opacity=0.9)

        poly2_12=Polygon(D, N, F)
        poly2_12.set_stroke(color=BLACK, width = 0.)
        poly2_12.set_fill(color = GOLD_E, opacity=0.5)

        poly3=Polygon(D, F, K)
        poly3.set_stroke(color=BLACK, width = 0.)
        poly3.set_fill(color = RED_E, opacity=0.9)

        poly3w=Polygon(D, K, F)
        poly3w.set_stroke(color=BLACK, width = 0.)
        poly3w.set_fill(color = WHITE, opacity=0.9)

        poly4=Polygon(D, K, B)
        poly4.set_stroke(color=BLACK, width = 0.)
        poly4.set_fill(color = RED_E, opacity=0.9)

        poly4w=Polygon(D, K, B)
        poly4w.set_stroke(color=BLACK, width = 0.)
        poly4w.set_fill(color = WHITE, opacity=0.9)

        poly5=Polygon(D, B, L)
        poly5.set_stroke(color=BLACK, width = 0.)
        poly5.set_fill(color = GREEN_E, opacity=0.9)

        poly5d=Polygon(K, B, L)
        poly5d.set_stroke(color=BLACK, width = 0.)
        poly5d.set_fill(color = GREEN_E, opacity=0.9)

        poly6=Polygon(D, L, I)
        poly6.set_stroke(color=BLACK, width = 0.)
        poly6.set_fill(color = GREEN_E, opacity=0.9)

        poly6_4=Polygon(D, K, I)
        poly6_4.set_stroke(color=BLACK, width = 0.)
        poly6_4.set_fill(color = GOLD_E, opacity=0.5)

        poly7=Polygon(D, I, M)
        poly7.set_stroke(color=BLACK, width = 0.)
        poly7.set_fill(color = RED_E, opacity=0.9)

        poly7w=Polygon(D, I, M)
        poly7w.set_stroke(color=BLACK, width = 0.)
        poly7w.set_fill(color = WHITE, opacity=0.9)

        poly8=Polygon(D, M, A)
        poly8.set_stroke(color=BLACK, width = 0.)
        poly8.set_fill(color = RED_E, opacity=0.9)

        poly8d=Polygon(J, M, A)
        poly8d.set_stroke(color=BLACK, width = 0.)
        poly8d.set_fill(color = RED_E, opacity=0.9)

        poly8dw=Polygon(J, A, M)
        poly8dw.set_stroke(color=BLACK, width = 0.)
        poly8dw.set_fill(color = WHITE, opacity=0.9)

        poly9=Polygon(D, A, J)
        poly9.set_stroke(color=BLACK, width = 0.)
        poly9.set_fill(color = GREEN_E, opacity=0.9)

        poly9_7=Polygon(D, I, J)
        poly9_7.set_stroke(color=BLACK, width = 0.)
        poly9_7.set_fill(color = GOLD_E, opacity=0.5)

        poly10=Polygon(D, J, E)
        poly10.set_stroke(color=BLACK, width = 0.)
        poly10.set_fill(color = GREEN_E, opacity=0.9)

        poly11=Polygon(D, E, N)
        poly11.set_stroke(color=BLACK, width = 0.)
        poly11.set_fill(color = RED_E, opacity=0.9)

        poly11w=Polygon(D, N, E)
        poly11w.set_stroke(color=BLACK, width = 0.)
        poly11w.set_fill(color = WHITE, opacity=0.9)

        poly12=Polygon(D, N, C)
        poly12.set_stroke(color=BLACK, width = 0.)
        poly12.set_fill(color = RED_E, opacity=0.9)

        poly12w=Polygon(D, N, C)
        poly12w.set_stroke(color=BLACK, width = 0.)
        poly12w.set_fill(color = WHITE, opacity=0.9)

        poly1_2=Polygon(D, C, F)
        poly1_2.set_stroke(color=BLACK, width = 0.3)
        poly1_2.set_fill(color = GREEN_E, opacity=0.9)

        poly3_4=Polygon(D, F, B)
        poly3_4.set_stroke(color=BLACK, width = 0.3)
        poly3_4.set_fill(color = RED_E, opacity=0.9)

        poly5_6=Polygon(D, B, I)
        poly5_6.set_stroke(color=BLACK, width = 0.3)
        poly5_6.set_fill(color = GREEN_E, opacity=0.9)

        poly7_8=Polygon(D, I, A)
        poly7_8.set_stroke(color=BLACK, width = 0.3)
        poly7_8.set_fill(color = RED_E, opacity=0.9)

        poly9_10=Polygon(D, A, E)
        poly9_10.set_stroke(color=BLACK, width = 0.3)
        poly9_10.set_fill(color = GREEN_E, opacity=0.9)

        poly11_12=Polygon(D, E, C)
        poly11_12.set_stroke(color=BLACK, width = 0.3)
        poly11_12.set_fill(color = RED_E, opacity=0.9)

        dt=1.

        self.play(ShowCreation(poly1_2), run_time=0.7)
        self.play(ShowCreation(poly3_4), run_time=0.7)
        self.play(ShowCreation(poly5_6), run_time=0.7)
        self.play(ShowCreation(poly7_8), run_time=0.7)
        self.play(ShowCreation(poly9_10), run_time=0.7)
        self.play(ShowCreation(poly11_12), run_time=0.7)
        self.play(Write(title2))
        self.wait(2.)
        self.play(*map(FadeOut, [title2]), run_time=0.5)
        self.play(FadeIn(poly1), FadeIn(poly2), FadeIn(poly3), FadeIn(poly4), FadeIn(poly5), FadeIn(poly6), FadeIn(poly7), FadeIn(poly8), FadeIn(poly9), FadeIn(poly10), FadeIn(poly11), FadeIn(poly12), run_time=dt)

        self.remove(poly1_2, poly3_4, poly5_6, poly7_8, poly9_10, poly11_12)
        self.play(ShowCreation(D0), ShowCreation(F0), ShowCreation(I0), ShowCreation(E0), ShowCreation(lineDF), ShowCreation(lineDI), ShowCreation(lineDE), run_time=dt)
        self.wait(0.5)
        self.play(ShowCreation(lineJK), ShowCreation(J0), ShowCreation(K0))
        self.play(ShowCreation(lineDN), ShowCreation(N0))

        self.play(ShowCreation(lineJM), ShowCreation(lineKL), ShowCreation(lineNO), ShowCreation(L0), ShowCreation(M0), ShowCreation(O0), run_time=0.5)
        self.play(ShowCreation(lineDM), ShowCreation(lineDL), ShowCreation(lineDO), run_time=0.5)


        self.play(ReplacementTransform(poly6,poly6_4), run_time=4.)

        self.play(ReplacementTransform(poly6_4,poly4w), run_time=4.)
        self.play(FadeIn(K0), FadeIn(B0), FadeIn(D0), FadeIn(lineKL), FadeIn(lineAB), FadeIn(lineBC), run_time=dt)

        self.play(ReplacementTransform(poly9,poly9_7), run_time=4.)
        self.play(ReplacementTransform(poly9_7,poly7w), run_time=4.)
        self.play(FadeIn(M0), FadeIn(I0), FadeIn(D0), FadeIn(lineAB), FadeIn(lineDI), FadeIn(lineDM), FadeIn(lineDA), run_time=dt)

        self.play(ReplacementTransform(poly2,poly2_12), run_time=4.)

        self.play(ReplacementTransform(poly2_12,poly12w), run_time=4.)
        self.play(FadeIn(C0), FadeIn(N0), FadeIn(D0), FadeIn(O0), FadeIn(lineNO), FadeIn(lineCA), FadeIn(lineDC), run_time=dt)

        self.play(ReplacementTransform(poly1,poly1d), run_time=3.)
        self.play(FadeIn(C0), FadeIn(N0), FadeIn(O0), FadeIn(lineDB), run_time=dt)

        self.play(ReplacementTransform(poly5,poly5d), run_time=3.)
        self.play(FadeIn(L0), FadeIn(K0), FadeIn(B0), run_time=dt)

        self.play(ReplacementTransform(poly8,poly8d), run_time=3.)
        self.play(FadeIn(A0), FadeIn(M0), FadeIn(J0), FadeIn(lineDA), run_time=dt)

        self.play(ReplacementTransform(poly10,poly11w), run_time=4.)
        self.play(FadeIn(N0), FadeIn(D0), FadeIn(E0), FadeIn(lineDE), FadeIn(lineDN), FadeIn(lineCA), run_time=dt)

        self.play(ReplacementTransform(poly1d,poly3w), run_time=4.)
        self.play(FadeIn(D0), FadeIn(F0), FadeIn(K0), FadeIn(lineJK), FadeIn(lineDF), FadeIn(lineBC), run_time=dt)

        self.play(ReplacementTransform(poly5d,poly8dw), run_time=4.)
        self.play(FadeIn(A0), FadeIn(M0), FadeIn(J0), FadeIn(lineJM), FadeIn(lineAB), FadeIn(lineCA), FadeIn(lineDA), run_time=dt)