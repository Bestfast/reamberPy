from __future__ import annotations

from typing import List

import pandas as pd

from reamber.base.Note import Note
from reamber.base.lists.TimedList import TimedList


class NoteList(TimedList[Note]):
    def max_column(self) -> int: ...
    def in_columns(self, columns: List[int]) -> NoteList: ...
    @property
    def column(self) -> pd.Series: ...
    @column.setter
    def column(self, val) -> None: ...
    @property
    def offset(self) -> pd.Series: ...
    @offset.setter
    def offset(self, val) -> None: ...