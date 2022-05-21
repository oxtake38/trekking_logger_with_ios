import sys
import os

from decimal import Decimal, ROUND_HALF_UP

import pytest

sys.path.append(os.getcwd())
from src import calculation

@pytest.mark.parametrize("point_1, point_2, expected", [
    ({"latitude":100.0, "longitude":50.0}, {"latitude":120.0, "longitude":50.0}, 2231.0668),
    ({"latitude":100.0, "longitude":50.0}, {"latitude":100.0, "longitude":25.0}, 481.1137)
])
def test_calc_distance(point_1, point_2, expected):
    actual = calculation.calc_distance(point_1, point_2)
    assert Decimal(str(actual)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)==Decimal(str(expected)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
