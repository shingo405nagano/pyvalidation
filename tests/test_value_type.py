import numpy as np
import pytest

from pyvalidation.utils.value_type import (
    IsColor,
    iterable_specific_type,
    scale_to_0_to_1,
    scale_to_8bit,
    value_range_0_to_1,
    value_range_8bit,
    value_range_16bit,
)


@pytest.mark.parametrize(
    "value, expected",
    [
        (-0.1, False),
        (0, True),
        (0.5, True),
        (1.0, True),
        (1.5, False),
    ],
)
def test_value_range_0_to_1(value, expected):
    """Test the value_range_0_to_1 function."""
    assert value_range_0_to_1(value) == expected
    with pytest.raises(TypeError):
        value_range_0_to_1("string")
    with pytest.raises(TypeError):
        value_range_0_to_1([0.5])


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1, False),
        (0, True),
        (128, True),
        (255, True),
        (256, False),
        (1000, False),
    ],
)
def test_value_range_8bit(value, expected):
    """Test the value_range_8bit function."""
    assert value_range_8bit(value) == expected
    with pytest.raises(TypeError):
        value_range_8bit("string")
    with pytest.raises(TypeError):
        value_range_8bit([128])


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1, False),
        (0, True),
        (32768, True),
        (65535, True),
        (65536, False),
        (100000, False),
    ],
)
def test_value_range_16bit(value, expected):
    """Test the value_range_16bit function."""
    assert value_range_16bit(value) == expected
    with pytest.raises(TypeError):
        value_range_16bit("string")
    with pytest.raises(TypeError):
        value_range_16bit([32768])


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, 0),
        (0.5, 127),
        (1.0, 255),
        (0.1, 25),
        (0.9, 229),
    ],
)
def test_scale_to_8bit(value, expected):
    """Test the scale_to_8bit function."""
    assert scale_to_8bit(value) == expected
    assert scale_to_8bit(1.5) is False
    assert scale_to_8bit(-0.1) is False
    with pytest.raises(TypeError):
        scale_to_8bit("string")
    with pytest.raises(TypeError):
        scale_to_8bit([0.5])


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0.0),
        (127, 0.4980392156862745),
        (255, 1.0),
        (25, 0.09803921568627451),
        (229, 0.8980392156862745),
    ],
)
def test_scale_to_0_to_1(value, expected):
    """Test the scale_to_0_to_1 function."""
    assert scale_to_0_to_1(value) == expected
    assert scale_to_0_to_1(256) is False
    assert scale_to_0_to_1(-1) is False
    with pytest.raises(TypeError):
        scale_to_0_to_1("string")
    with pytest.raises(TypeError):
        scale_to_0_to_1([127])


@pytest.mark.parametrize(
    "iterable, type_, expected",
    [
        ([1.0, 1.0, 0.0], int, False),
        ([1.0, 1.0, 0.0], float, True),
        ([1, 2, 3], int, True),
        ([1, 2, 3], float, False),
        (['1', '2', '3'], str, True),
        ('a', str, False),
        (np.array([1, 2, 3]), int, True),
    ],
)
def test_iterable_specific_type(iterable, type_, expected):
    """Test the iterable_specific_type function."""
    assert iterable_specific_type(iterable, type_) == expected


@pytest.mark.parametrize(
    "color, expected",
    [
        ((255, 0, 0), True),
        ((255, 255, 255), True),
        ("red", True),
        ('black', True),
        ("#FF0000", True),
        ("#00FF00", True),
        ('##00ff00', None),
        ('string', None),
    ]
)
def test_is_color(color, expected):
    if expected is None:
        with pytest.raises(ValueError):
            IsColor(color=color)
    else:
        is_color = IsColor(color=color)
        assert is_color.is_color == expected


@pytest.mark.parametrize(
    "color, mpl_range, expected",
    [
        ('red', True, (1.0, 0.0, 0.0)),
        ('red', False, (255, 0, 0)),
    ]
)
def test_is_color_rgb(color, mpl_range, expected):
    is_color = IsColor(color=color)
    assert is_color.rgb(mpl_range) == expected


@pytest.mark.parametrize(
    "color, alpha, mpl_range, expected",
    [
        ('red', 1.0, True, (1.0, 0.0, 0.0, 1.0)),
        ('red', 0.5, True, (1.0, 0.0, 0.0, 0.5)),
        ('red', 1.0, False, (255, 0, 0, 255)),
        ('red', 0.5, False, (255, 0, 0, 127)),
        ('red', 1.1, True, None)
    ]
)
def test_is_color_rgba(color, alpha, mpl_range, expected):
    is_color = IsColor(color=color)
    if expected is not None:
        assert is_color.rgba(alpha=alpha, mpl_range=mpl_range) == expected
    else:
        with pytest.raises(ValueError):
            is_color.rgba(alpha=alpha, mpl_range=mpl_range)


@pytest.mark.parametrize(
    "color, alpha, expected",
    [
        ('red', 1.0, '#0000ffff'),
        ('red', 0.5, '#0000ff7f'),
        ('red', 0.0, '#0000ff00'),
    ]
)
def test_is_color_bgra(color, alpha, expected):
    is_color = IsColor(color=color)
    assert is_color.bgra(alpha=alpha) == expected
