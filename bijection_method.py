from manim import *
from manim.typing import Vector2D, Vector3D
from manim.utils.rate_functions import ease_out_bounce
#from voiceOver import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
#from manim_voiceover.services.pyttsx3 import PyTTSX3Service
from voiceOver import VoiceoverScene
import numpy as np
from typing import Any, Sequence
from numpy import array as arr
from scipy.interpolate import CubicSpline
import dialogue as dia
import extra
import func
from extra import ExtraScene, PDot, moveScaleToFit
axis_config={"include_ticks":True,"numbers_with_elongated_ticks":[1,3],}
background_line_style={"stroke_opacity":0}
textColor={'f':YELLOW,'x':RED,'y':GREEN,'a':GREY,'b':GREY_BROWN}
extra.MathTexColorDictConfig.update(textColor)
positiveAxis=extra.axis2D(x_range=(-1,5,1),y_range=(-2,4,1),)
config.tex_template.add_to_preamble(r"\usepackage{xcolor}")


class BijectionMethod(VoiceoverScene):
    def construct(self):
        #self.set_speech_service(GTTSService())
        headline=Text(dia.HEADLINE,font_size=60).to_edge(UP)
        with self.voiceover(dia.HEADLINE) as tracker:
            self.play(FadeIn(headline,scale=1.5),run_time=tracker.duration)
        self.wait(1)
        with self.voiceover(dia.ROOT_FINDING+dia.WHICH_MEANS1) as tracker:
            self.wait(tracker.duration)
        l=(
                MathTex(r'f(x)=0',substrings_to_isolate='fxy')
                .set_color_by_tex_to_color_map(textColor)
                .to_corner(LEFT)
                .next_to(headline,DOWN,coor_mask=np.array([0,1,1]))
            )
        with self.voiceover(dia.WHICH_MEANS2) as trac:
            self.play(Create(l))
        with self.voiceover(dia.TWOCONDITION) as trac:
            self.wait(trac.duration)
        with self.voiceover(dia.CONDITION1) as trac:
            rul1=(extra.markDown(r"""1. There exist $a$ and $b$ so that,
                                $f(a)$ and $f(b)$ are of different signs""")
                  .next_to(l,DOWN)
                  .align_to(l,LEFT)
                  )
            self.play(Write(rul1),run_time=trac.duration/1.5)
            objs=extra.drawGraphPoint(
                    positiveAxis.copy(),
                    x_point=[1,4],
                    y_point=[4,-1],
                    )

            objs.group.scale(0.3).next_to(rul1,RIGHT) 
            objs.anim(self)
            self.wait(1)
        with self.voiceover(dia.CONDITION2) as trac:
            rul2=(extra.markDown(r"""2. The function $f$ has to be continious on range a to b""",)
                    .next_to(objs.group,DOWN)
                    .to_edge(LEFT)
                  )
            self.play(Write(rul2),run_time=trac.duration/1.5)

        with self.voiceover(dia.FOCUS) as trac:
            self.play(*[Uncreate(x) for x in [rul1,headline,objs.group,l]])
            self.play(rul2.animate.to_edge(UP)) #type: ignore

class ExplainContinious(VoiceoverScene):
    def construct(self):
       # self.set_speech_service(GTTSService())
        rul2=extra.markDown(r"""2. The function $f$ has to be continious on range a to b""").to_edge(UP)
        self.add(rul2)
        with self.voiceover(dia.CONTINIOUS_DES) as trac:
            self.wait(trac.duration)
        with self.voiceover(dia.CONTI_EXAMPLE) as trac:
            exampleFunc=CubicSpline(x=[0,2,3],y=[1,0,-2])
            axes=positiveAxis.copy().next_to(rul2,DOWN)
            graph=axes.plot(exampleFunc,x_range=(0,3)) #type: ignore
            endPoints=extra.addEndPoints(graph)
            drawGraph=graph.copy().set_color(GREEN)
            graph.set_color(RED)
            self.play(extra.sequentialAnimation([axes,endPoints,graph]),run_time=4)
        with self.voiceover(dia.CONTI_REASON) as trac:
            pen=extra.Pen()
            pen=pen.shift(endPoints[0].get_center()-pen.get_corner(DL)) #type: ignore
            self.play(Write(pen),run_time=trac.duration/2)
            self.play(extra.DrawUsingCorner(drawGraph,pen,DL)
                      ,run_time=trac.duration/2)
            self.remove(graph)
        self.play(Unwrite(VGroup(drawGraph,endPoints)),run_time=2)
        with self.voiceover(dia.NOT_CONTI) as trac:
            func1=CubicSpline(x=[0,1,2],y=[-2,2,1])
            func2=CubicSpline(x=[2,3,4],y=[0,1,3])
            graph1=axes.plot(func1,x_range=(0,2)).set_color(RED)#type: ignore
            drawGraph=graph1.copy().set_color(GREEN)
            graph2=axes.plot(func2,x_range=(2,4)).set_color(RED)#type: ignore
            endPoint1=extra.addEndPoints(graph1)
            endPoint2=extra.addEndPoints(graph2)
            graphs=VGroup(endPoint1,endPoint2,graph1,graph2)
            self.play(Write(graphs))
            self.play(pen.animate.shift(endPoint1[0].get_center()-pen.get_corner(DL))) #type: ignore
            self.play(extra.DrawUsingCorner(drawGraph,pen,DL),rate_func=ease_out_bounce,run_time=trac.duration)
        with self.voiceover(dia.NOT_CONTI2) as trac:
            self.wait(trac.duration)
graph=extra.axis2D([-1,7,1],[-6,6,1],unitSize=(1,0.5))
c2p=graph.c2p

class FunctionIntersect(VoiceoverScene):
    def construct(self):
        #self.set_speech_service(GTTSService())
        #self.set_speech_service(NoOpService())
        self.next_section(skip_animations=False)
        with self.voiceover(dia.THINK_ABOUT) as trac:
            self.wait(trac.duration/2)
            self.play(Create(graph))
        with self.voiceover(dia.POINT_A) as trac:
            aPos=arr((1,3,0))
            a=Dot(c2p(*aPos))

            lA=extra.label("A",a,LEFT)
            vA=graph.get_vertical_line(a.get_center())
            self.play(Create(vA))
            self.play(Create(VGroup(a,lA)))
        with self.voiceover(dia.POINT_B) as trac:
            bPos=arr((5,-2,0))
            b=Dot(c2p(*bPos))

            lB=extra.label("B",b,RIGHT)
            vB=graph.get_vertical_line(b.get_center())
            self.play(Create(vB))
            self.play(Create(VGroup(b,lB)))
        with self.voiceover(dia.A_TO_B) as trac:
            Ca=ValueTracker(0)
            C=arr([[1.5,4],
                   [2.5,-3.5],
                   [4,3]])
            Cf=lambda:func.multilerp(C,Ca.get_value())
            ax,ay,_=aPos
            bx,by,_=bPos
            def f():
                cx,cy=Cf()
                return CubicSpline(x=[ax,cx,bx],y=[ay,cy,by],)
            def plotDraw():
                func=f()
                roots=[x for x in func.roots() if ax<=x<=bx]
                dots=VGroup(*[Dot(c2p(x,0)) for x in roots])
                plot=graph.plot(func,[ax,bx])
                return VGroup(dots,plot)
            plot=always_redraw(plotDraw)
            self.play(Create(plot))
            self.play(Ca.animate.set_value(2),run_rate=linear,run_time=trac.duration/2)
            self.play(Ca.animate.set_value(0),run_rate=linear,run_time=trac.duration/2)
        self.play(FadeOut(plot))

class RootMiddle(ExtraScene,MovingCameraScene):
    def construct(self):
        #self.set_speech_service(GTTSService())
        self.next_section(skip_animations=False)
        with self.voiceover(dia.FOR_A_FUNCTION) as trac:
            self.add(graph)
            ax=ValueTracker(1)
            bx=ValueTracker(6)
            axDot=always_redraw(lambda :PDot(c2p(ax.get_value(),0)))
            bxDot=always_redraw(lambda :PDot(c2p(bx.get_value(),0)))
            self.add(axDot,bxDot)
            tipA=extra.tipTo(axDot,DOWN,text='a',updater=True)
            tipB=extra.tipTo(bxDot,UP,text='b',updater=True)
            self.play(FadeIn(tipA.group),FadeIn(tipB.group),point_color=RED)
            root=ValueTracker(2)
            rootDot=always_redraw(lambda:PDot(c2p(root.get_value(),0)))
            rootTip=extra.tipTo(rootDot,DOWN,text='root',updater=True)
            self.add(rootDot)
            self.play(Create(rootTip.group))
            self.wait(1)
            self.play(root.animate.set_value(5))
            self.wait(1)
            self.play(root.animate.set_value(3))
        with self.voiceover(dia.ROOT_RENAME) as trac:
            assert rootTip.text is not None
            self.play(Transform(rootTip.text,extra.markDown('$x$').move_to(rootTip.text)))
        with self.voiceover(dia.ROOT_IS) as trac:
            eqXeq=extra.markDownC(r"$x =$")
            eqAvg=extra.markDownC(r"$\frac {a+b}{2}$").next_to(eqXeq,RIGHT)
            eq1=VGroup(eqXeq,eqAvg)
            pm= MathTex(r"\pm").next_to(eqAvg,RIGHT)
            eqDif=extra.markDownC(r"$\frac {|a-b|}{2}$").next_to(pm,RIGHT)
            eq2= VGroup(pm,eqDif)
            eq=VGroup(eq1,eq2).center().next_to(rootTip.group,DOWN,coor_mask=arr([0,1,1]))
            self.play(Write(eq1))
        with self.voiceover(dia.WITH_ERROR) as trac:
            self.play(Write(eq2))

        with self.voiceover(dia.CELEBRATE) as trac:
            self.play(Circumscribe(eq))
        with self.voiceover(dia.NOT_SATISFACTORY) as trac:
            pass

        changedVar=Group(graph,ax,bx).save_state()
        with self.voiceover(dia.SATIFY_IF) as trac:
            self.play(ax.animate.set_value(2.8),
                      bx.animate.set_value(3.4),
                      root.animate.set_value(3.1),
#                      tipA.group.animate.scale(0.3),
#                      tipB.group.animate.scale(0.3),
#                      rootTip.group.animate.scale(0.3),
                    )
            zoomTo=Group(axDot,bxDot)
            scaleOp=extra.moveScaleToFit(zoomTo,self.getScreenRectangle(),1)
            self.play(scaleOp.animate(graph))
            self.wait(3)
        with self.voiceover(dia.ERROR_LESS) as trac:
            brace=Brace(Group(rootDot,bxDot),buff=0.05)
            self.play(GrowFromCenter(brace))
            errorText=eqDif.copy()
            brace.put_at_tip(errorText,buff=0.05)
            self.play(ReplacementTransform(eqDif.copy(),errorText))
        self.play(Restore(changedVar))
        self.play(FadeOut(brace,errorText,rootTip.group,eq))

        self.next_section(skip_animations=False)
        with self.voiceover(dia.MAKE_SMALL) as trac:
            pass
        with self.voiceover(dia.MORE_INFOR) as trac:
            pass
        with self.voiceover(dia.CHOOSE_MIDDLE) as trac:
            root.set_value((ax.get_value()+bx.get_value())/2)
            rootDot=always_redraw(lambda:Dot(c2p(root.get_value(),0),color=textColor['x']))

            xLabel=extra.label("$x$",rootDot,DR,True)
            self.play(GrowFromCenter(rootDot),GrowFromCenter(xLabel))
                        
        with self.voiceover(dia.THREE_STATE) as trac:
            funcDot=always_redraw(lambda:Dot(c2p(root.get_value(),3),color=textColor['x']))
            animDot=rootDot.copy()
            line=always_redraw(lambda:DashedLine(rootDot,animDot,))
            #The value can be positive
            self.add(animDot,line)
            self.play(Transform(animDot,funcDot))

            fxLabel=extra.label("$f(x)$",animDot,UR)
            self.play(Write(fxLabel))
            #Or it can be negative
            funcDot1=always_redraw(lambda:Dot(c2p(root.get_value(),-2),color=textColor['x']))
            animDot1=rootDot.copy()
            line1=always_redraw(lambda:DashedLine(rootDot,animDot1,))
            self.add(animDot1,line1)
            self.play(Transform(animDot1,funcDot1))

            fxLabel1=extra.label("$f(x)$",animDot1,DR)
            self.play(Write(fxLabel1))

            #or it can be zero,in which case we found the value of root
            self.play(Transform(animDot,rootDot),Transform(animDot1,rootDot))

            self.play(FadeOut(fxLabel,fxLabel1))
        with self.voiceover(dia.NEW_RANGE_POS) as trac:
            self.play(Transform(animDot,funcDot))
            #We found a new range of a and b where x became the new a
            self.play(Circumscribe(Group(rootDot,bxDot)))
            #We know the root is somewhere in this region.
        with self.voiceover(dia.NEW_RANGE_NEG) as trac:
            #if it is negative,
            self.play(Transform(animDot,funcDot1))
            #then we know that the root will be in this region.
            self.play(Circumscribe(Group(rootDot,axDot)))

class IterationAnimation(extra.ExtraScene):
    def construct(self):
        f=lambda x:-.5*(x-2.1)*(x-3.1)*(x-4.8)
        self.add(graph)
        with self.voiceover("Enough theory,Let's go to an example.I have drawn a function in the graph") as trac:
            funcPlot=graph.plot(f,[0,7,0.1],True)
            self.play(Create(funcPlot))
            graph.add(funcPlot)
        with self.voiceover("Let's say we found out two value a and b for which the function outputs poistive and negative value") as trac:
            vA,vB=[1,6]
            graphPoints=extra.drawGraphPoint(graph,[vA,vB],[f(vA),f(vB),],pointUpdater=True)
            axDot,bxDot=graphPoints.axisDots
            faxDot,fbxDot=graphPoints.funcDots
            axDots=VGroup(axDot,faxDot)
            bxDots=VGroup(bxDot,fbxDot)
            aLabel=extra.label("$a$",axDot,DL,True)
            bLabel=extra.label("$b$",bxDot,DR,True)
            self.play(FadeIn(axDot,bxDot,aLabel,bLabel))
            graphPoints.anim(self)
        with self.voiceover("Now if a and b are close enough,we get a good approximation for x but here it isn't.") as trac:
            pass
        with self.voiceover("So we will take look at the middle of a and b and find the value of the function there.") as trac:
            def generatePoint(x:float):
                xPoint=extra.drawGraphPoint(graph,[x],[f(x)],pointUpdater=True)
                xDot=xPoint.axisDots
                fxDot=xPoint.funcDots
                xLabel=extra.label("$x$",xDot,DR,True)
                self.play(GrowFromCenter(xDot))
                self.play(Circumscribe(xDot))
                self.play(Write(xLabel))
                xPoint.anim(self)
                return VGroup(xLabel,VGroup(xDot,fxDot))
            vX=(vA+vB)/2
            fX=f(vX)
            xLabel,xDots=generatePoint(vX)
            xDot,fxDot=xDots
        with self.voiceover("As the value is positive,We got a smaller from x to b,where x is positive and b is negative.") as trac:
            self.play(Circumscribe(Group(xDot,bxDot)))
        with self.voiceover("So we have to find the root inside it.Let's zoom in here for a bit.") as trac:
            #anim=extra.moveZoomToFit(VGroup(xDots,bxDots),self.get_screenRectangle(),0.3)
            anim=self.cameraZoomToFit(VGroup(xDots,bxDots),fixedY=True)
            self.play(anim.animate(graph))
        with self.voiceover("For simplicity let's rename the x to a") as trac:
            self.play(aLabel.animate.move_to(xLabel),FadeOut(xLabel))
            vA=vX
            axDots=xDots
            axDot=xDot
            
        with self.voiceover("Repeat this pattern over and over again") as trac:
            for i in range(10):
                vX=(vA+vB)/2
                fX=f(vX)
                xLabel,xDots=generatePoint(vX)
                xDot,fxDot=xDots
                if fX==0:break
                if fX>0:
                    self.play(Circumscribe(Group(xDot,bxDot)))
                    anim=self.cameraZoomToFit(VGroup(xDots,bxDots),fixedY=True)
                    self.play(anim.animate(graph))
                    self.remove(aLabel)
                    self.play(xLabel.animate.become(extra.label("$a$",xDot,DL,updater=True)))
                    vA=vX
                    axDots=xDots
                    axDot=xDot
                else:
                    self.play(Circumscribe(Group(xDot,axDot)))
                    anim=self.cameraZoomToFit(VGroup(xDots,axDots),fixedY=True)
                    self.play(anim.animate(graph))

                    self.remove(bLabel)
                    self.play(xLabel.animate.become(extra.label("$b$",xDot,DR,updater=True)))
                    vB=vX
                    bxDots=xDots
                    bxDot=xDot


class ErrorRecap(VoiceoverScene):
    def construct(self):
        #self.set_speech_service(GTTSService())
        config.tex_template.add_to_preamble(r"\usepackage{xcolor}")
        with self.voiceover(dia.ERROR_EXP) as trac:
            eq=extra.markDown(r"$x= a \pm b$")
            eq1=extra.markDown(r"$\implies a-b \leq x \leq a+b$")
            xeq=r"$x=$"
            aba=r"$\frac{a+b}{2}$"
            abd=r"$\frac{b-a}{2}$"
            pm=r"$\pm$"
            eq2=extra.markDownC(xeq,aba,pm,abd)
            eq3=extra.markDownC(aba,'-',abd,r'$\leq$','$x$',r'$\leq$',aba,'+',abd)
            eq4=extra.markDownC(r"$a \leq x \leq b$")
            VGroup(eq,eq1,eq2,eq3,eq4).arrange(DOWN).to_corner(UP)
            self.play(FadeIn(eq),run_time=trac.duration/4)
            self.play(TransformMatchingTex(eq.copy(),eq1),run_time=trac.duration*3/4)
        with self.voiceover(dia.ERROR_EXP2) as trac:
            self.play(FadeIn(eq2),run_time=trac.duration/4)
            self.play(TransformMatchingTex(eq2.copy(),eq3),run_time=trac.duration*3/4)
        self.play(FadeIn(eq3.copy(),eq4),run_time=3)
        #self.play(Create(VGroup(eq,eq1)))


class TestRender(Scene):
    def construct(self):
        axes=positiveAxis.copy()

