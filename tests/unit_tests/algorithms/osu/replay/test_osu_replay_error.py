import pickle
from collections import defaultdict
from dataclasses import field

import numpy as np
from osrparse import Replay, ReplayEventMania, Mod, parse_replay_file

from reamber.algorithms.osu.OsuReplayError import OsuReplayError
from reamber.osu import OsuMap
from tests.unit_tests.conftest import MAPS_DIR, REPS_OSU_DIR

MAP_PATH = MAPS_DIR / "osu/MAGiCVLGiRL_ZVPH.osu"
REPS_PATH = REPS_OSU_DIR / "MAGiCVLGiRL_ZVPH.osu/"


def test_replay():
    errors = OsuReplayError(
        [r.as_posix() for r in REPS_PATH.glob("*.osr")],
        MAP_PATH.as_posix()
    ).errors()
    with open("errors.pkl", "rb+") as f:
        errors_exp = pickle.load(f)

    for act, exp in zip(errors.errors, errors_exp.errors):
        for ar_act, ar_exp in zip(act.hits.values(), exp.hits.values()):
            assert all(ar_act == ar_exp)

        for ar_act, ar_exp in zip(act.releases.values(),
                                  exp.releases.values()):
            assert all(ar_act == ar_exp)

