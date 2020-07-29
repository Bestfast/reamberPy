from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from dataclasses import dataclass
if TYPE_CHECKING:
    from reamber.algorithms.storyboard.StoryBoard import StoryBoard

@dataclass
class SBEvent:
    pass

@dataclass
class SBEMove(SBEvent):
    fromX: float = 0.0
    fromY: float = 0.0
    toX: float = 0.0
    toY: float = 0.0

    def moveBy(self, x:float = 0.0, y:float = 0.0):
        self.toX = self.fromX + x
        self.toY = self.fromY + y

    def reverse(self):
        x_ = self.fromX
        y_ = self.fromY
        self.fromX = self.toX
        self.fromY = self.toY
        self.toX = x_
        self.toY = y_

@dataclass
class SBEFade(SBEvent):
    fromA: float = 1.0
    toA: float = 1.0

    def reverse(self):
        a_ = self.fromA
        self.fromA = self.toA
        self.toA = a_

@dataclass
class SBEScale(SBEvent):
    fromX: float = 1.0
    fromY: float = 1.0
    toX: float = 1.0
    toY: float = 1.0

    def setFrom(self, scale):
        self.fromX = scale
        self.fromY = scale

    def setTo(self, scale):
        self.toX = scale
        self.toY = scale

    def reverse(self):
        x_ = self.fromX
        y_ = self.fromY
        self.fromX = self.toX
        self.fromY = self.toY
        self.toX = x_
        self.toY = y_
