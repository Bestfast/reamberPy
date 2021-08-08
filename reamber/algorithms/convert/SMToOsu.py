from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.osu.OsuMap import OsuMap
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.sm.SMMapSet import SMMapSet


class SMToOsu(ConvertBase):
    @classmethod
    def convert(cls, sm: SMMapSet) -> List[OsuMap]:
        """ Converts a SMMapset to possibly multiple osu maps

        Note that a mapset contains maps, so a list would be expected.
        SMMap conversion is not possible due to lack of SMMapset Metadata
        """

        # I haven't tested with non 4 keys, so it might explode :(

        osus: List[OsuMap] = []
        for sm in sm.maps:
            osu = OsuMap()
            osu.hits = cls.cast(sm.hits, OsuHitList, dict(offset='offset', column='column'))
            osu.holds = cls.cast(sm.holds, OsuHoldList, dict(offset='offset', column='column', length='length'))
            osu.bpms = cls.cast(sm.bpms, OsuBpmList, dict(offset='offset', bpm='bpm'))

            osu.background_file_name = sm.background,
            osu.title = sm.title,
            osu.title_unicode = sm.title_translit,
            osu.artist = sm.artist,
            osu.artist_unicode = sm.artist_translit,
            osu.audio_file_name = sm.music,
            osu.creator = sm.credit,
            osu.version = f"{sm.difficulty} {sm.difficulty_val}",
            osu.preview_time = int(sm.sample_start),

            osus.append(osu)
        return osus
