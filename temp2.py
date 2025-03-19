from manim import *

class Anim(Scene):
    def construct(self):
        axes=Axes()
        c2p=axes.c2p 
        xList=[ValueTracker(1),ValueTracker(6)]
        dotList=[always_redraw(lambda:Dot(c2p(x.get_value(),0))) for x in xList]
        self.add(*dotList)
        self.wait()
        self.play(axes.animate.shift(UR))


