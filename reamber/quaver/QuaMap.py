from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Union

import yaml
from yaml import CLoader, CDumper, CSafeLoader

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.quaver.QuaBpm import QuaBpm
from reamber.quaver.QuaHit import QuaHit
from reamber.quaver.QuaHold import QuaHold
from reamber.quaver.QuaMapMeta import QuaMapMeta
from reamber.quaver.QuaSv import QuaSv
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.QuaSvList import QuaSvList

DEFAULT_MISSING = 0

@dataclass
class QuaMap(QuaMapMeta, Map):

    notes: QuaNotePkg = field(default_factory=lambda: QuaNotePkg())
    bpms:  QuaBpmList = field(default_factory=lambda: QuaBpmList())
    svs:   QuaSvList  = field(default_factory=lambda: QuaSvList())

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms,
                'svs': self.svs}

    @staticmethod
    def read(lines: Union[List[str], str], safe: bool = True) -> QuaMap:
        """ Reads a .qua, loads inplace, hence it doesn't return anything

        Safe loading is slower, however, it's safer, it uses yaml.CSafeLoader
        Unsafe loading is faster, however it's unsafe, it uses yaml.CLoader

        :param lines: The lines of the .qua file. If it's in a list, it'll be joined for compatibility with pyyaml
        :param safe: If the source is trusted, you can put as False, probably faster"""

        self = QuaMap()

        # Note that do not strip, YAML uses whitespaces.

        file = yaml.load(lines if isinstance(lines, str) else "\n".join(lines) + "\n",
                         Loader=CSafeLoader if safe else CLoader)

        # We pop them so as to reduce the size needed to pass to _readMeta
        self._read_notes(file.pop('HitObjects'))
        self._read_bpms(file.pop('TimingPoints'))
        self._read_svs(file.pop('SliderVelocities'))
        self._read_metadata(file)

        return self

    @staticmethod
    def read_file(file_path: str) -> QuaMap:
        """ Reads a .qua, loads inplace, hence it doesn't return anything

        :param file_path: The path to the .qua file."""

        with open(file_path, "r", encoding="utf-8") as f:
            # Reading with CReader is much faster
            file = f.read().split("\n")

        return QuaMap.read(file)

    def write_file(self, file_path: str):
        """ Writes a .qua, doesn't return anything.

        :param file_path: The path to a new .qua file."""
        file = self._write_meta()

        bpm: QuaBpm
        file['TimingPoints'] = [bpm.as_dict() for bpm in self.bpms]
        sv: QuaSv
        file['SliderVelocities'] = [sv.as_dict() for sv in self.svs]
        note: Union[QuaHit, QuaHold]

        # This long comprehension squishes the hits: {} and holds: {} to a list for as_dict operation
        # noinspection PyTypeChecker
        file['HitObjects'] = [i.as_dict() for j in [v for k, v in self.notes.data().items()] for i in j]
        with open(file_path, "w+", encoding="utf8") as f:
            # Writing with CDumper is much faster
            f.write(yaml.dump(file, default_flow_style=False, sort_keys=False, Dumper=CDumper,allow_unicode=True))

    def _read_bpms(self, bpms: List[Dict]):
        for bpm in bpms:
            self.bpms.append(QuaBpm(offset=bpm.get('StartTime', DEFAULT_MISSING),
                                    bpm=bpm.get('Bpm', DEFAULT_MISSING)))

    def _read_svs(self, svs: List[Dict]):
        for sv in svs:
            self.svs.append(QuaSv(offset=sv.get('StartTime', DEFAULT_MISSING),
                                  multiplier=sv.get('Multiplier', DEFAULT_MISSING)))

    def _read_notes(self, notes: List[Dict]):
        for note in notes:
            offset = note.get('StartTime', DEFAULT_MISSING)
            column = note['Lane'] - 1
            key_sounds = note['KeySounds']
            if "EndTime" in note.keys():
                self.notes.holds().append(QuaHold(offset=offset,
                                                  _length=note.get('EndTime', DEFAULT_MISSING) - offset,
                                                  column=column, key_sounds=key_sounds))
            else:
                self.notes.hits().append(QuaHit(offset=offset, column=column, key_sounds=key_sounds))

    def scroll_speed(self, center_bpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType. Overrides the base to include SV

        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param center_bpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """

        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if center_bpm is None: center_bpm = 1

        sv_pairs = [(offset, multiplier) for offset, multiplier in zip(self.svs.sorted().offset,
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

        return formatting(self.artist, self.title, self.difficulty_name, self.creator)

    def rate(self, by: float):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        """
        return super(QuaMap, self).rate(by=by)
