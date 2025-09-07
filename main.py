from manim import *
from scenes.intro import IntroScene
from scenes.outro import OutroScene 
from scenes.main_scenes import s1_launch, s2_orbit, s3_transfer

class MasterScene(MovingCameraScene):
    def construct(self):
        IntroScene.construct(self)
        s1_launch(self)       # Scene 1
        s2_orbit(self)        # Scene 2
        s3_transfer(self)     # Scene 3
        OutroScene.construct(self)
