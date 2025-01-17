import pandas as pd

from reamber.sm.lists.SMBpmList import SMBpmList


def test_type(sm_map):
    assert isinstance(sm_map.bpms.df, pd.DataFrame)


def test_df_names(sm_map):
    assert {'offset', 'metronome', 'bpm'} == set(sm_map.bpms.df.columns)
