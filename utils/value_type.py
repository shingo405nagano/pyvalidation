from typing import Any, Callable, Type

import numpy as np
from matplotlib.colors import to_hex, to_rgb, to_rgba

from pyvalidation.utils.config import Numeric, UniqueIterable
from pyvalidation.utils.dimansional import dimensional_count


def is_numeric(func: Callable) -> Callable:
    """
    ## Summary:
        Decorator to check if a value is numeric.
    Arguments:
        func (function):
            The function to be decorated.
    Returns:
        function: The decorated function.
    """

    def wrapper(value: Numeric) -> bool:
        if not isinstance(value, (int, float)):
            raise TypeError(
                f"Value must be an int or float, not {type(value).__name__}"
            )
        return func(value)

    return wrapper


@is_numeric
def value_range_8bit(value: Numeric) -> bool:
    """
    ## Summary:
        Check if a value is within the 8-bit range.
    Arguments:
        value (int | float):
            The value to be measured.
    """
    return 0 <= value <= 255


@is_numeric
def value_range_16bit(value: Numeric) -> bool:
    """
    ## Summary:
        Check if a value is within the 16-bit range.
    Arguments:
        value (int | float):
            The value to be measured.
    """
    return 0 <= value <= 65535


@is_numeric
def value_range_0_to_1(value: Numeric) -> bool:
    """
    ## Summary:
        Check if a value is within the range of 0 to 1.
    Arguments:
        value (int | float):
            The value to be measured.
    """
    return 0 <= value <= 1


def scale_to_8bit(value: float) -> int | bool:
    """
    ## Summary:
        Scale a value from 0-1 to 0-255.
    Args:
        value (float):
            The value to be scaled. Value must be between 0 and 1.
    Returns:
        int | bool: 
            Scaled value in the range of 0 to 255.
            If the value is not in the range of 0 to 1, return False.
    """
    if value_range_0_to_1(value):
        return int(value * 255)
    return False


def scale_to_0_to_1(value: int) -> float | bool:
    """
    ## Summary:
        Scale a value from 0-255 to 0-1.
    Args:
        value (int):
            The value to be scaled. Value must be between 0 and 255.
    Returns:
        float | bool: 
            Scaled value in the range of 0 to 1.
            If the value is not in the range of 0 to 255, return False.
    """
    if value_range_8bit(value):
        return value / 255
    return False


def iterable_specific_type(value: UniqueIterable, type_: Type) -> bool:
    """
    ## Summary:
        Check if all items in a list are of a specific type.
    Arguments:
        value (tuple | list | np.ndarray | pd.Series):
            The list to be measured.
        type_ (Type):
            The type to check for.
    Returns:
        bool: True if all items are of the specified type, False otherwise.
    """
    np_types = {
        np.integer: int,
        np.int8: int,
        np.int16: int,
        np.int32: int,
        np.int64: int,
        np.floating: float,
        np.float16: float,
        np.float32: float,
        np.float64: float,
        np.str_: str,
    }
    dimensional = dimensional_count(value)
    if 0 < dimensional < 3:
        new_value = []
        for item in value:
            if type(item) in np_types:
                new_value.append(np_types.get(type(item))(item))
            else:
                new_value.append(item)
        return all(isinstance(item, type_) for item in new_value)
    return False


class IsColor():
    def __init__(self, color: Any):
        self.is_color = False
        self.color = self._validate_color(color)

    def _validate_color(self, color: Any) -> str:
        """
        ## Summary:
            Validate if the value is a valid color.
        Args:
            color (str | tuple):
                The value to be validated.
        Returns:
            str: 
                Hexadecimal color value.
        """
        try:
            dimensional = dimensional_count(color)
            if dimensional == 1:
                if iterable_specific_type(color, int):
                    color = [scale_to_0_to_1(v) for v in color]
            # Use `to_hex` to check if it is valid as a color.
            color = to_hex(color)
        except Exception as e:
            raise ValueError(
                f"Invalid color value. arg: {color}, type: {type(color)}, error: {e}")
        else:
            self.is_color = True
            return color

    def _scale_to_8bit(self, value: tuple[float]) -> tuple[int]:
        """
        ## Summary:
            0 to 1 value to 8-bit value.
        Args:
            value (tuple[float, float, float]):
                The value to be converted.
        Returns:
            tuple[int, int, int]: 
                8-bit color value.
        """
        return tuple([scale_to_8bit(v) for v in value])

    def rgb(self, mpl_range: bool = True) -> tuple[float] | tuple[int]:
        """
        ## Summary:
            Convert the color to RGB format.
        Args:
            mpl_range (bool):
                If True, return the value in the range of 0 to 1.
                If False, return the value in the range of 0 to 255.
        Returns:
            tuple[float, float, float]: 
                RGB color value.
        """
        rgb_ = to_rgb(self.color)
        return rgb_ if mpl_range else self._scale_to_8bit(rgb_)

    def rgba(self, alpha: float = 1.0, mpl_range: bool = True) -> tuple[float] | tuple[int]:
        """
        ## Summary:
            Convert the color to RGBA format.
        Args:
            alpha (float):
                The alpha value to be used.
            mpl_range (bool):
                If True, return the value in the range of 0 to 1.
                If False, return the value in the range of 0 to 255.
        Returns:
            tuple[float]: 
                RGBA color value.
        """
        if value_range_0_to_1(alpha):
            rgba_ = to_rgba(self.color, alpha=alpha)
            return rgba_ if mpl_range else self._scale_to_8bit(rgba_)
        else:
            raise ValueError("Alpha value must be between 0 and 1.")

    def bgra(self, alpha: float = 1.0) -> str:
        """
        ## Summary:
            Convert the color to BGRA format. BGRA is used in GoogleEarth.
        Args:
            alpha (float):
                The alpha value to be used. Value must be between 0 and 1.
        Returns:
            str: 
                Hexadecimal color value. Value is in BGRA format.
        """
        r, g, b, a = self.rgba(alpha=alpha, mpl_range=False)
        return "#" + ''.join([f"{int(v):02x}" for v in [b, g, r, a]])
