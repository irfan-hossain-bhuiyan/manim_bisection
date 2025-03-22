from manim import *
import extra as et

class InterpolateExample(Scene):
    def construct(self):
        pass
class MaxRectExample(et.ExtraScene):
    def construct(self):
        innerRect=Rectangle(color=PINK,height=3,width=5)
        innerRectDot=Dot(UR)
        anim=self.cameraZoomToFit(innerRect,buff=0,fixedX=True,fixedY=False
                                  ,pivot=innerRectDot.get_center())
        self.wait(4)
        self.play(anim.animate(VGroup(innerRect,innerRectDot)))
        self.wait(4)
        

        #g=VGroup(rect,d).shift(UR)
        #anim=self.cameraZoomToFit(g,fixedX=False,fixedY=False,pivot=d.get_center())
        #self.play(anim.animate(g))
        #self.wait(4)

