from manim import mobject
from manim.typing import Point2D, Point2DLike, Vector3D,Point3D
import numpy as np

from numpy.typing import ArrayLike, NDArray
from numpy import array as arr
import re
from typing import Callable, Dict,List, Sequence, Type,Tuple
from dataclasses import dataclass
from manim import *
# Example usage:
from typing import Any, Iterable,List,Dict
from itertools import chain
import tempfile
import re
STR_COLOR_MAP=Dict[str,ManimColor]
ArgDict=Dict[str,Any]|None
MathTexColorDictConfig:STR_COLOR_MAP=dict()
PDot=lambda *x:Dot(point=x,radius=0,fill_opacity=0)
def sometimesDraw(func:Callable[[],Mobject],updater:bool=False):
    obj=func()
    setattr(obj,"isUpdating",updater)
    def update(x):
        if x.isUpdating:
            obj.become(func())
    obj.add_updater(update)
    return obj
    
def point_to_ratio(rect: Mobject, point:Point2D) -> Point2D:
    """
    Given a rectangle (assumed axis-aligned) and a point,
    return the point's ratio within the rectangle.
    
    The ratio is (0,0) at the rectangle's bottom-left corner
    and (1,1) at the top-right corner.
    
    Parameters:
        rect (Mobject): The rectangle object.
        point (np.ndarray): The point's coordinates.
        
    Returns:
        np.ndarray: The ratio of the point as a numpy array [ratio_x, ratio_y, point_z].
    """
    # Get the bottom left and top right corners of the rectangle.
    bottom_left = rect.get_corner(DL)
    top_right = rect.get_corner(UR)
    
    # Calculate the ratios.

    ratio=(point-bottom_left)/(top_right-bottom_left)
    # Return the ratio, preserving the z-coordinate.
    return ratio
def ratio_to_point(rect:Mobject,ratio:Point2D)->Point2D:
    space=np.array([rect.height,rect.width])
    return rect.get_corner(DL)+space*ratio
    
def get_mobject_key(mobject: Mobject,rounding:int=3) -> int:
    """
        Unique key for close object

        >>> get_mobject_key(Circle()) == get_mobject_key(Circle().shift(UP))
        true
    """
    mobject.save_state()
    mobject.center()
    mobject.set(height=1)
    result = hash(np.round(mobject.points, rounding).tobytes())
    mobject.restore()
    return result
def test_get_mobject_key():
    assert get_mobject_key(Circle()) == get_mobject_key(Circle().shift(UP))
from contextlib import contextmanager
import manim as mm
class ExtraScene(mm.Scene):
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
    def get_screenRectangle(self):
        if not hasattr(self.camera,"frame_height") or not hasattr(self.camera,"frame_width"):
            raise ValueError
        return Rectangle(height=getattr(self.camera,"frame_height"),width=getattr(self.camera,"frame_width"))
    def cameraZoomToFit(self,obj:Mobject,buff:float=0.0,fixedX=False,fixedY=False,pivot:None|Point2D=None):
        screenRect=self.get_screenRectangle()
        ratio=np.ones_like(2)*0.5 if pivot is None else point_to_ratio(obj,pivot)
        objRect=SurroundingRectangle(obj,buff=0)
        d=Dot(objRect.get_center() if pivot is None else pivot)
        prG=VGroup(objRect,d)
        mask=np.ones(3)
        if fixedX:
            mask[0]=0
        if fixedY:
            mask[1]=0
        prG.move_to(ORIGIN,mask)
        self.add(prG)
        self.wait()
        toRect=max_rect_inside(screenRect,d.get_center(),ratio)
        self.add(toRect)
        self.wait()
        return moveZoomToFit(objRect,toRect)



        #pivot=obj.get_center() if pivot is None else pivot
        #rel_pivot=point_to_ratio(obj,pivot)
        #if  not fixedX:
        #    pivot[0]=0
        #if not fixedY:
        #    pivot[1]=0
        #rect_to_go=max_rect_inside(screenRect,pivot,rel_pivot)
        #return moveZoomToFit(obj,rect_to_go,buff)
        
class Tracker:
    def __init__(self,scene:mm.Scene,duration:float):
        self._start=scene.renderer.time
        self._end=self._start+duration
        self._scene=scene
        self.duration=duration
    def get_remaining_duration(self)->float:
        return max(self._end-self._scene.renderer.time,0)

def axis2D(x_range:Sequence,y_range:Sequence,unitSize:ArrayLike=1):
    x_ulength=x_range[1]-x_range[0]
    y_ulength=y_range[1]-y_range[0]
    ulength=arr([x_ulength,y_ulength])
    x_lenght,y_length=ulength*arr(unitSize)
    return Axes(x_range=x_range,y_range=y_range,x_length=x_lenght,y_length=y_length)

def markDown(*text: str, colorDict:STR_COLOR_MAP=MathTexColorDictConfig,**kwargs)->MathTex:
    """
        kwargs:
            colorDict: Dict[str,ManimColor]=MathTexColorDictConfig
            tex_environment: str = "align*",
    """
    separators = set(colorDict.keys())
    parsed_text = [_mdtoL(t, separators) for t in text if t]
    return MathTex(*chain.from_iterable(parsed_text),**kwargs).set_color_by_tex_to_color_map(colorDict,substring=False) 

def markDownC(*text: str, colorDict:STR_COLOR_MAP=MathTexColorDictConfig,**kwargs)->MathTex:
    """
        kwargs:
            colorDict: Dict[str,ManimColor]=MathTexColorDictConfig
            tex_environment: str = "align*",
    """
    return MathTex(*[_mdtoLc(x,colorDict)for x in text],**kwargs) 



@dataclass
class DGP:
    group:VGroup
    axisDots:VGroup
    funcDots:VGroup
    animValue:Mobject
    animDots:VGroup
    lines:VGroup
    axes:Axes
    anim:Callable[[Scene],None]
def drawGraphPoint(axes:Axes,
                   x_point:List[float],
                   y_point:List[float],
                   point:Dot=Dot(),
                   line:Callable[[Point3D,Point3D],Line]=DashedLine,
                   pointUpdater=True
                   )->DGP:
    c2p=axes.c2p
    gpoint=lambda x,y:point.copy().move_to(c2p(x,y))
    axisDots=VGroup(*[gpoint(x,0) for x in x_point])
    funcDots=VGroup(*[gpoint(x,y) for x,y in zip(x_point,y_point)])
    animValue=ValueTracker(0)
    animDots=axisDots.copy()
    if pointUpdater:
        for x,xV in zip(axisDots,x_point):
            x.add_updater(lambda x,xV=xV:x.move_to(axes.c2p(xV,0)))
        for x,xV,yV in zip(funcDots,x_point,y_point):
            x.add_updater(lambda x,xV=xV,yV=yV:x.move_to(axes.c2p(xV,yV)))
        for ani,x,y in zip(animDots,axisDots,funcDots):
            ani.add_updater(lambda ani,xC=x,yC=y:ani.move_to(interpolate(xC.get_center(),yC.get_center(),animValue.get_value())))

    gline=lambda x,y:always_redraw(lambda:line(x.get_center()
                                                ,y.get_center()
                                               )
                                   )
    lines=VGroup(*[gline(x,y) for x,y in zip(axisDots,animDots)])

    group=VGroup(axisDots,funcDots,animDots,lines,axes)
    def createAnim(scene:Scene):
        scene.add(animDots,funcDots)
        scene.add(*lines)
        scene.play(animValue.animate.set_value(1))

    return DGP(group=group,
               axisDots=axisDots,
               funcDots=funcDots.set_opacity(0),
               animValue=animValue,
               animDots=animDots,
               lines=lines,
               axes=axes,
               anim=createAnim,
            )
    
 
def label(text:str,
          obj:Mobject,
          side:Vector3D,
          updater=False,
          colorDict:STR_COLOR_MAP=MathTexColorDictConfig,
          **kwargs)->MathTex:
    t=markDown(text,colorDict=colorDict,**kwargs).next_to(obj,side)
    if updater:
        t.add_updater(lambda x:x.become(x.next_to(obj,side)))
    return t



def _mdtoL(text: str, separator:set[str]) -> List[str]:
    parts = text.split('$')
    ans = []
    for i, t in enumerate(parts):
        if not t:  # Skip empty strings
            continue
        if i%2==0:
            ans.append('\\\\\n'.join([r"\text{" + x + "}" if x.strip() else "" for x in t.split('\n') ]))
        else:
            ans.extend(split_text(t, separator))
    return ans

def test_mdtoL():
    MathTexColorDictConfig.update({'f':YELLOW,'x':RED,'y':GREEN,'a':GREY,'b':GREY_BROWN})
    xeq=r"$x=$"
    aba=r"$\frac{a+b}{2}$"
    abd=r"$\frac{b-a}{2}$"
    pm= r"$\pm$"
    assert list(_mdtoL(xeq,set(MathTexColorDictConfig.keys())))==['x', '=']
    assert list(_mdtoL(aba,set(MathTexColorDictConfig.keys())))==['\\frac{', 'a', '+', 'b', '}{2}']
    assert list(_mdtoL(abd,set(MathTexColorDictConfig.keys())))==['\\frac{', 'b', '-', 'a', '}{2}']
    assert list(_mdtoL(pm ,set(MathTexColorDictConfig.keys())))==['\\pm']

def _mdtoLc(text:str,colorDict:STR_COLOR_MAP=MathTexColorDictConfig):
    split_text=_mdtoL(text,set(colorDict.keys()))
    ans=[]
    for x in split_text:
        color=colorDict.get(x)
        if color:
            x=fr"\textcolor[HTML]{{{color.to_hex()[1:]}}}{{{x}}}"
        ans.append(x)
    return "".join(ans)
def test_mdtoLc():
    MathTexColorDictConfig.clear()
    MathTexColorDictConfig.update({'f':YELLOW,'x':RED,'y':GREEN,'a':GREY,'b':GREY_BROWN})
    xeq=r"$x=$"
    aba=r"$\frac{a+b}{2}$"
    abd=r"$\frac{b-a}{2}$"
    pm= r"$\pm$"
    assert [
    _mdtoLc(xeq),
    _mdtoLc(aba),
    _mdtoLc(abd),
    _mdtoLc(pm ),
    ]==['\\textcolor[HTML]{FC6255}{x}=', '\\frac{\\textcolor[HTML]{888888}{a}+\\textcolor[HTML]{736357}{b}}{2}',
     '\\frac{\\textcolor[HTML]{736357}{b}-\\textcolor[HTML]{888888}{a}}{2}', '\\pm']

def _find_matching_prefix(text, prefixes):
    for prefix in prefixes:
        if text.startswith(prefix):
            return prefix
    return ""
def split_text(text: str, substrings: set[str]) -> Iterable[str]:
    """
    Split the string based on substrings.It doesn't split if the substrings are part of words
    in latex context,So thingas like split_text("hello l world",["l"])->["hello","l","world"]
        """
    if not substrings:
        yield text
        return
    i=j=0

    while j<len(text):
        a=_find_matching_prefix(text[j:],substrings)
        if not a:
            j+=1
            continue
        if j!=0 and (text[j-1].isalnum() or text[j-1]=='/'):
            j+=1
            continue
        n=len(a)+j
        if n<len(text) and text[n].isalnum():
            j+=1
            continue
        if i!=j:yield text[i:j]
        yield text[j:n]
        i=j=n
    if i!=j:
        yield text[i:j]
def test_split_text():
    MathTexColorDictConfig.clear()
    MathTexColorDictConfig.update({'f':YELLOW,'x':RED,'y':GREEN,'a':GREY,'b':GREY_BROWN})
    xeq=r"$x=$"
    aba=r"$\frac{a+b}{2}$"
    abd=r"$\frac{b-a}{2}$"
    pm= r"$\pm$"
    assert list(split_text(xeq,set(MathTexColorDictConfig.keys())))==['$', 'x', '=$']
    assert list(split_text(aba,set(MathTexColorDictConfig.keys())))==['$\\frac{', 'a', '+', 'b', '}{2}$']
    assert list(split_text(abd,set(MathTexColorDictConfig.keys())))==['$\\frac{', 'b', '-', 'a', '}{2}$']
    assert list(split_text( pm,set(MathTexColorDictConfig.keys())))==['$\\pm$']


class DrawCurveWithDot(Animation):
    def __init__(self, curve: VMobject, penTip: Mobject,offset:Vector3D=ORIGIN,**kwargs):
        # Save a copy of the full (undrawn) curve
        self.full_curve = curve.copy()
        self.pentip = penTip
        self.curve= curve
        self.offset=offset
        # We animate the curve (self.mobject)
        super().__init__(Group(curve,penTip), **kwargs)
    def interpolate_mobject(self, alpha: float) -> None:
        # Update the animated curve to show only the subcurve from 0 to alpha.
        alpha=self.rate_func(alpha)
        self.curve.pointwise_become_partial(self.full_curve,0, alpha)
        # Move the dot along the full curve.
        self.pentip.move_to(self.full_curve.point_from_proportion(alpha)+self.offset)


def Pen(penColor:ParsableManimColor=WHITE,penWidth:float|None=None):
    with tempfile.NamedTemporaryFile(suffix='.svg') as temp:
        temp.write(b"""<?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
<svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M15.2869 3.15178L14.3601 4.07866L5.83882 12.5999L5.83881 12.5999C5.26166 13.1771 4.97308 13.4656 4.7249 13.7838C4.43213 14.1592 4.18114 14.5653 3.97634 14.995C3.80273 15.3593 3.67368 15.7465 3.41556 16.5208L2.32181 19.8021L2.05445 20.6042C1.92743 20.9852 2.0266 21.4053 2.31063 21.6894C2.59466 21.9734 3.01478 22.0726 3.39584 21.9456L4.19792 21.6782L7.47918 20.5844L7.47919 20.5844C8.25353 20.3263 8.6407 20.1973 9.00498 20.0237C9.43469 19.8189 9.84082 19.5679 10.2162 19.2751C10.5344 19.0269 10.8229 18.7383 11.4001 18.1612L11.4001 18.1612L19.9213 9.63993L20.8482 8.71306C22.3839 7.17735 22.3839 4.68748 20.8482 3.15178C19.3125 1.61607 16.8226 1.61607 15.2869 3.15178Z" stroke="#1C274C" stroke-width="1.5"/>
<path opacity="0.5" d="M14.36 4.07812C14.36 4.07812 14.4759 6.04774 16.2138 7.78564C17.9517 9.52354 19.9213 9.6394 19.9213 9.6394M4.19789 21.6777L2.32178 19.8015" stroke="#1C274C" stroke-width="1.5"/>
</svg>""")
        temp.flush()
        pen=SVGMobject(temp.name).set_stroke(color=penColor,width=penWidth)
        return pen

def DrawUsingCorner(obj:VMobject,penPin:Mobject,criticalDir:Vector3D):
    offset=penPin.get_corner(criticalDir)-penPin.get_center()
    return DrawCurveWithDot(obj,penPin,-offset)


def addEndPoints(obj:Mobject,point:Callable=Dot):
    return VGroup(*[point(x) for x in obj.get_start_and_end()])

def sequentialAnimation(obj:List[Mobject],anim:Type[Animation]=Create):
    return Succession(*map(anim,obj)) #type: ignore

def directionToTheta(direction:NDArray):
    return np.arctan2(direction[1],direction[0])
d2t=directionToTheta

@dataclass
class TipToR:
    group:VGroup
    text:MathTex|None
    tip:ArrowTip

def tipTo(obj:Mobject|Vector3D,direction:Vector3D,
          tip:type[ArrowTip]=ArrowTriangleFilledTip,
          text:str="",
          updater=False,
          tipSettings:ArgDict=None,
          textSettings:ArgDict=None)->TipToR:
    """ 
        tipSettings:
            fill_opacity: float = 0,
            stroke_width: float = 3,
            length: float = DEFAULT_ARROW_TIP_LENGTH,
            width: float = DEFAULT_ARROW_TIP_LENGTH,

        textSettings:
            colorDict: Dict[Tuple[str,...]|str,ParsableManimColor]|Any|None=MathTexColorDictConfig
            tex_environment: str = "align*",
"""
    tipSettings=tipSettings or {}
    textSettings=textSettings or {}
    t=tip(start_angle=-d2t(direction),**tipSettings).next_to(obj,direction)
    if text:
        txt=markDown(text,**textSettings).next_to(t,direction)
        group=VGroup(t,txt)
    else:
        group=VGroup(t)
        txt=None
    if updater:
        group.add_updater(lambda x:x.next_to(obj,direction))
    return TipToR(group=group,tip=t,text=txt)
@dataclass
class MoveRotSca:
    def __init__(self,move=ORIGIN,rotate:float=0.0,scale:float=1.0,pivot=None) -> None:
        """
            Doing shift,rotate and scale operation in one go

            pivot=None if the operation is center of the object,A Vector3d otherwise.
        """
        self.move:Point3D=move
        self.rotate:float=rotate
        self.scale:float=scale
        self.pivot:Vector3D|None=pivot
    def apply(self,obj:Mobject,center:Point3D|None=None):
        if center is None:
            return obj.scale(self.scale).rotate(self.rotate).shift(self.move)
        return obj.scale(self.scale,about_point=center).rotate(self.rotate,about_point=center).shift(self.move)
    def animate(self,obj:Mobject):
        if self.pivot is None:
            return obj.animate.scale(self.scale).rotate(self.rotate).shift(self.move)
        return obj.animate.scale(self.scale,about_point=self.pivot).rotate(self.rotate,about_point=self.pivot).shift(self.move)

    
def moveZoomToFit(obj:Mobject,toObj:Mobject,buff:float=0.0,):
    """
        Gives the move and scale operation to fit to the object,
        The operation should be done from center
    """

    scale=min((toObj.width-buff)/obj.width,(toObj.height-buff)/obj.height)
    move=toObj.get_center()-obj.get_center()*scale
    return MoveRotSca(move,0,scale,pivot=ORIGIN)
def max_rect_inside(outer_rect: Rectangle, point: Point3D,pointRatio:Point2DLike=(0.5,0.5), buffer: float = 0.0) -> Rectangle:
    # Get the outer rectangle boundaries
    left = outer_rect.get_left()[0]+buffer
    right = outer_rect.get_right()[0]-buffer
    bottom = outer_rect.get_bottom()[1]+buffer
    top = outer_rect.get_top()[1]-buffer
    del buffer
    clampPositive=lambda x:max(0,x)
    widthLeft=clampPositive(point[0]-left)
    widthRight=clampPositive(right-point[0])
    heightUp=clampPositive(top-point[1])
    heightDown=clampPositive(point[1]-bottom)
    # Compute the available half-dimensions from the center to the edges
    width_available = min(widthLeft/pointRatio[0],widthRight/(1-pointRatio[0]))
    #height_available = min((top - point[1])/pointRatio[1], (point[1] - bottom)/(1-pointRatio[1]))
    height_available = min(heightDown/pointRatio[1],heightUp/(1-pointRatio[1]))
    
    # Subtract the buffer (ensuring they don't go negative)
    dotLD=PDot((point[0]-width_available*pointRatio[0],point[1]-height_available*pointRatio[1],0))
    dotRU=PDot((point[0]+width_available*(1-pointRatio[0]),point[1]+height_available*(1-pointRatio[1]),0))
    inner_rect=SurroundingRectangle(VGroup(dotLD,dotRU),buff=0)
    # Create the new rectangle using the buffered dimensions
    return inner_rect
def get_inner_rectangle(rect: Rectangle, buffer: float) -> Rectangle:
        # Calculate new dimensions ensuring a buffer from each side.
        new_width = rect.get_width() - 2 * buffer
        new_height = rect.get_height() - 2 * buffer
        
        # Create a new rectangle with the calculated dimensions,
        # and align its center to the center of the outer rectangle.
        return Rectangle(width=new_width, height=new_height).move_to(rect.get_center())

class Demo(ExtraScene):
    def construct(self):
        graph=axis2D([-1,7,1],[-6,6,1],unitSize=(1,0.5))
        c=drawGraphPoint(graph,[1,3],[2,4],pointUpdater=True)
        self.add(graph)
        self.add(c.axisDots,c.funcDots)        
        c.anim(self)
        self.play(self.cameraZoomToFit(VGroup(c.axisDots,c.funcDots),fixedY=True))
        self.wait(3)
        
def main():
    MathTexColorDictConfig.update({'f':YELLOW,'x':RED,'y':GREEN,'a':GREY,'b':GREY_BROWN})
if __name__=="__main__":
    main()

