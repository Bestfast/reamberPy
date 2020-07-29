from reamber.base.Map import Map
from reamber.algorithms.storyboard.SBDrawable import SBDrawable



class StoryBoard:

    def __add__(self, other: SBDrawable):
        assert isinstance(other, SBDrawable), "The added class must be an instance of SBDrawable!"
        return other.draw(sb=self)

    def __init__(self,
                 m: Map):

        self.m = m

