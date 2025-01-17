from __future__ import annotations

from typing import List

from reamber.osu.OsuHit import OsuHit
from reamber.osu.lists.notes.OsuNoteList import OsuNoteList


class OsuHitList(OsuNoteList[OsuHit]):

    @staticmethod
    def read(strings: List[str], keys: int) -> OsuHitList: ...

    def write(self, keys: int) -> List[str]: ...

    @staticmethod
    def read_editor_string(s: str) -> OsuHitList: ...
