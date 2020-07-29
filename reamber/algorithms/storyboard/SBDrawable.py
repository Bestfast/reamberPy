from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reamber.algorithms.storyboard.StoryBoard import StoryBoard

class SBDrawable(ABC):
    """ All Storyboard Drawing classes must inherit from this to enable the __add__ op """
    @abstractmethod
    def draw(self, sb: 'StoryBoard') -> 'StoryBoard': ...
