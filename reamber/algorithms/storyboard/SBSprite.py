from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from reamber.algorithms.storyboard.SBEvent import SBEvent
from typing import List


@dataclass
class SBSprite:
    fileName: str = ""
    events: List[SBEvent] = field(default_factory=lambda: [])
