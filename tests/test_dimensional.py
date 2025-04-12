from pyvalidation.dimansional import dimensional_count
import pytest
import numpy as np
import datetime


@pytest.mark.parametrize(
    "iterable, expected",
    [
        ([0, 1, 2], 1),
        ([[0, 1], [2, 3]], 2),
        ([[[0], [1]], [[2], [3]]], 3),
        (np.array([0, 1, 2]), 1),
        (np.array([[0, 1], [2, 3]]), 2),
        (np.array([[[0], [1]], [[2], [3]]]), 3),
        (datetime.datetime.now(), 0),
        ('list[0, 0]', 0),
    ]
)
def test_dimensional_count(iterable, expected):
    """Test the dimensional_count function."""
    assert dimensional_count(iterable) == expected
