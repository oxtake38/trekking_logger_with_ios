import sys
import os

import pytest

sys.path.append(os.getcwd())
from src import util

def test_t():
    assert util.t()==4