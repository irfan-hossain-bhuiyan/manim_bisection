
from manim import *
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover import VoiceoverScene
class TestRender(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        c=Circle()
        s=Square()
        self.next_section(skip_animations=True)
        with self.voiceover("The circle is created.But it should be skipped."):
            self.play(Create(c))

        self.next_section(skip_animations=False)
        with self.voiceover("the square is drawn"):
            self.play(Create(s))
        self.wait(5)

