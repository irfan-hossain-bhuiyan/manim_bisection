from manim import *
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover import VoiceoverScene
class TestRender(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        c=Circle()
        s=Square()
        self.next_section(skip_animations=True)
        self.add_sound("./media/voiceovers/the-circle-is-created-but-it-should-be-skipped-83798e03.mp3")
        self.play(Create(c))
        self.wait(4)

        self.next_section(skip_animations=False)
        self.add_sound("./media/voiceovers/the-square-is-drawn-017a5bbf.mp3")
        self.play(Create(s))
        self.wait(7)

