from contextlib import contextmanager
import manim as mm
import re
class VoiceoverScene(mm.Scene):
    def set_speech_service(*args):
        pass
    @contextmanager
    def voiceover(self,text:str,buff:float=0):
        text=re.sub(r' {3,}', '\n', text)
        duration=len(text)*0.1+buff
        txtObject=mm.Text(text,font_size=17)
        txtObject.set_z(10)
        txtObject.to_edge(mm.DOWN)
        self.add(txtObject)
        track=Tracker(self,duration)
        try:
            yield track
        finally:
            remainingDuration=track.get_remaining_duration()
            if remainingDuration>0:
                self.wait(remainingDuration)
            self.remove(txtObject)
class Tracker:
    def __init__(self,scene:mm.Scene,duration:float):
        self._start=scene.renderer.time
        self._end=self._start+duration
        self._scene=scene
        self.duration=duration
    def get_remaining_duration(self,buff:float=0.0)->float:
        return max(self._end-self._scene.renderer.time,0)

