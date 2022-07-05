from pathlib import Path

import pytest

from reamber.algorithms.convert import BMSToOsu
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import PFDrawBeatLines, PFDrawNotes, \
    PFDrawBpm
from reamber.bms.BMSMap import BMSMap
from tests.unit_tests.conftest import MAPS_DIR

THIS_DIR = Path(__file__).parent


@pytest.fixture()
def bms_map():
    return BMSMap.read_file(MAPS_DIR / "bms/nhelv.bme")


def test_first_hit(bms_map):
    assert bms_map.hits.first_offset() == pytest.approx(1200, abs=1)


def test_last_hit(bms_map):
    assert bms_map.hits.last_offset() == \
           pytest.approx(2 * 60000 + 11256, abs=2)


def test_write(bms_map):
    osu = BMSToOsu.convert(bms_map)
    osu.audio_file_name = "audio.mp3"
    osu.circle_size = 8
    osu.version = 'test'
    osu.creator = 'Evening'

    osu.beatmap_set_id = 1344506
    osu.write_file(
        "D:/Program Files/osu!/Songs/Silentroom_-_Nhelv/Silentroom - Nhelv (Evening) [test].osu")


def test_draw():
    bms = BMSMap.read_file(MAPS_DIR / "bms/nhelv.bme")
    # bms_map.write_file(MAP_WRITE)
    pf = PlayField(bms, padding=50) \
         + PFDrawBeatLines() \
         + PFDrawNotes() \
         + PFDrawBpm()
    pf.export_fold(max_height=2300).save("nhelv.png")
