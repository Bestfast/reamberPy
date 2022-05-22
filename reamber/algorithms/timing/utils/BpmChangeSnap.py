from __future__ import annotations

from dataclasses import dataclass

from reamber.algorithms.timing.utils.BpmChangeBase import BpmChangeBase
from reamber.algorithms.timing.utils.snap import Snap


@dataclass
class BpmChangeSnap(BpmChangeBase):
    snap: Snap
