from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Union

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuHit import OsuHit
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuMapMeta import OsuMapMeta
from reamber.osu.OsuNoteMeta import OsuNoteMeta
from reamber.osu.OsuSampleSet import OsuSampleSet
from reamber.osu.OsuSv import OsuSv
from reamber.osu.OsuTimingPointMeta import OsuTimingPointMeta
from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.OsuSvList import OsuSvList


@dataclass
class OsuMap(Map, OsuMapMeta):

    notes: OsuNotePkg = field(default_factory=lambda: OsuNotePkg())
    bpms:  OsuBpmList = field(default_factory=lambda: OsuBpmList())
    svs:   OsuSvList  = field(default_factory=lambda: OsuSvList())

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms,
                'svs': self.svs}

    def reset_all_samples(self, notes=True, samples=True) -> None:
        """ Resets all hitsounds and samples

        :param notes: Whether to reset hitsounds on notes
        :param samples: Whether to reset samples
        """
        if notes:
            for n in self.notes.hits():
                n.hitsound_file = ""
                n.sample_set = OsuSampleSet.AUTO
                n.hitsound_set = OsuSampleSet.AUTO
                n.custom_set = OsuSampleSet.AUTO
                n.addition_set = OsuSampleSet.AUTO

            for n in self.notes.holds():
                n.hitsound_file = ""
                n.sample_set = OsuSampleSet.AUTO
                n.hitsound_set = OsuSampleSet.AUTO
                n.custom_set = OsuSampleSet.AUTO
                n.addition_set = OsuSampleSet.AUTO

        if samples: self.samples.clear()

    @staticmethod
    def read(lines: List[str]) -> OsuMap:
        """ Reads a .osu, loads inplace, hence it doesn't return anything

        :param lines: The lines to the .osu file."""

        self = OsuMap()
        lines = [line.strip() for line in lines]  # Redundancy for safety

        try:
            ix_tp = lines.index("[TimingPoints]")
            ix_ho = lines.index("[HitObjects]")
        except ValueError:
            raise Exception("Incorrect File Format. Cannot find [TimingPoints] or [HitObjects].")

        self._read_file_metadata(lines[:ix_tp])
        self._read_file_timing_points(lines[ix_tp + 1:ix_ho])
        self._read_file_hit_objects(lines[ix_ho + 1:])

        return self

    @staticmethod
    def read_file(file_path: str) -> OsuMap:
        """ Reads a .osu, loads inplace, hence it doesn't return anything

        :param file_path: The path to the .osu file."""

        with open(file_path, "r", encoding="utf8") as f:
            # We read the file and firstly find the distinct sections
            # 1) Meta 2) Timing Points 3) Hit Objects

            file = [i.strip() for i in f.read().split("\n")]

        return OsuMap.read(lines=file)

    def write_file(self, file_path=""):
        """ Writes a .osu, doesn't return anything.

        :param file_path: The path to a new .osu file."""

        with open(file_path, "w+", encoding="utf8") as f:
            for s in self.write_meta_string_list():
                f.write(s + "\n")

            f.write("\n[TimingPoints]\n")
            for tp in self.bpms:
                assert isinstance(tp, OsuBpm)
                f.write(tp.write_string() + "\n")

            for tp in self.svs:
                assert isinstance(tp, OsuSv)
                f.write(tp.write_string() + "\n")

            f.write("\n[HitObjects]\n")
            for ho in self.notes.hits():
                f.write(ho.write_string(keys=int(self.circle_size)) + "\n")

            for ho in self.notes.holds():
                f.write(ho.write_string(keys=int(self.circle_size)) + "\n")

    def _read_file_metadata(self, lines: List[str]):
        """ Reads the metadata only, inclusive of Events """
        self.read_meta_string_list(lines)

    def _read_file_timing_points(self, lines: Union[List[str], str]):
        """ Reads all TimingPoints """
        lines = lines if isinstance(lines, list) else [lines]
        for line in lines:
            if OsuTimingPointMeta.is_slider_velocity(line):
                self.svs.append(OsuSv.read_string(line))
            elif OsuTimingPointMeta.is_timing_point(line):
                self.bpms.append(OsuBpm.read_string(line))

    def _read_file_hit_objects(self, lines: Union[List[str], str]):
        """ Reads all HitObjects """
        lines = lines if isinstance(lines, list) else [lines]
        for line in lines:
            if OsuNoteMeta.is_hit(line):
                self.notes.hits().append(OsuHit.read_string(line, int(self.circle_size)))
            elif OsuNoteMeta.is_hold(line):
                self.notes.holds().append(OsuHold.read_string(line, int(self.circle_size)))

    def scroll_speed(self, center_bpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType. Overrides the base to include SV
    
        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param center_bpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """
    
        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if center_bpm is None: center_bpm = 1
    
        sv_pairs = [(offset, multiplier) for offset, multiplier in zip(self.svs.sorted().offset(),
                                                                       self.svs.multipliers())]
        bpm_pairs = [(offset, bpm) for offset, bpm in zip(self.bpms.offsets, self.bpms.bpms)]
    
        curr_bpm_iter = 0
        next_bpm_offset = None if len(bpm_pairs) == 1 else bpm_pairs[1][0]
        speed_list = []
    
        for offset, sv in sv_pairs:
            while offset < bpm_pairs[0][0]:  # Offset cannot be less than the first bpm
                continue
            # Guarantee that svOffset is after first bpm
            if next_bpm_offset and offset >= next_bpm_offset:
                curr_bpm_iter += 1
                if curr_bpm_iter != len(bpm_pairs):
                    next_bpm_offset = bpm_pairs[curr_bpm_iter][0]
                else:
                    next_bpm_offset = None
            speed_list.append(dict(offset=offset, speed=bpm_pairs[curr_bpm_iter][1] * sv / center_bpm))
    
        return speed_list

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return:
        """

        def formatting(artist, title, difficulty, creator):
            return f"{artist} - {title}, {difficulty} ({creator})"

        if unicode: return formatting(self.artist_unicode, self.title_unicode, self.version, self.creator)
        else: return formatting(self.artist, self.title, self.version, self.creator)

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        # noinspection PyTypeChecker
        osu = super(OsuMap, self).rate(by=by)
        osu: OsuMap

        # We invert it so it's easier to cast on Mult
        by = 1 / by
        osu.samples.offsets *= by
        osu.preview_time *= by

        return osu

