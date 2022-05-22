from __future__ import annotations

from dataclasses import dataclass

from reamber.algorithms.timing.utils.BpmChangeOffset import BpmChangeOffset
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap



@dataclass
class BpmChange(BpmChangeOffset, BpmChangeSnap):
    pass
