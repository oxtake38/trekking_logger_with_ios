import sys
import os

import pytest

sys.path.append(os.getcwd())
from src import util

@pytest.mark.parametrize("sec, expected",[
    (10, "10sec"),
    (10.1, "10sec"),
    (10.9, "10sec"),
    (-1, None),
    (59.9, "59sec"),
    (60, "1min0sec"),
    (60.1, "1min0sec"),
    (3599.9, "59min59sec"),
    (3600, None),
]
)
def test_get_time_diff_str(sec, expected):
    if sec==-1:
        with pytest.raises(AssertionError):
            util.get_time_diff_str(sec)
        return
    if sec==3600:
        with pytest.raises(AssertionError):
            util.get_time_diff_str(sec)
        return

    actual = util.get_time_diff_str(sec)
    assert actual == expected