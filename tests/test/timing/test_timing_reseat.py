import pytest

from reamber.algorithms.timing.TimingMap import TimingMap
from tests.test.timing.test_cases import cases


@pytest.mark.parametrize(
    'case',
    cases
)
def test_reseat(case):
    assert case.bpm_changes_reseat_snap == \
           TimingMap.reseat_bpm_changes_snap(case.bpm_changes_snap)
