from manim import *
class CheckPoint(Scene):
    def construct(self):
        s=Text("a")
        self.play(Create(s))
        self.add_subcaption("It's working,The subtitle is here.",duration=1)
