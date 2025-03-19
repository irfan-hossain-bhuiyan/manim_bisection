from manim import *
import extra as et

class InterpolateExample(Scene):
    def construct(self):
        pass
class MaxRectExample(et.ExtraScene):
    def construct(self):
        rect=Rectangle()
        d=Dot(LEFT)
        g=VGroup(rect,d).shift(UR*.5)
        anim=self.cameraZoomToFit(g,fixedX=False,fixedY=False,pivot=d.get_center())
        self.play(anim.animate(g))
        self.wait(4)

