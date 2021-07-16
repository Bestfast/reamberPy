from __future__ import annotations

import pandas as pd

from reamber.base.Timed import Timed
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta

class OsuSv(OsuTimingPointMeta, Timed):

    def __init__(self, offset: float, multiplier: float = 1.0, metronome: int = 4, sample_set: int = OsuSampleSet.AUTO,
                 sample_set_index: int = 0, volume: int = 50, kiai: bool = False, **kwargs): ...
    @staticmethod
    def code_to_value(code: float) -> float: ...
    @staticmethod
    def value_to_code(value: float) -> float: ...
    @staticmethod
    def read_string(s: str) -> OsuSv or None: ...
    def write_string(self) -> str: ...
    @property
    def multiplier(self) -> pd.Series: ...
    @multiplier.setter
    def multiplier(self, val) -> None: ...

