from manim import *
val=ValueTracker(0)
val.save_state()
val.set_value(10)
print(val.get_value())
val.restore()
print(val.get_value())
