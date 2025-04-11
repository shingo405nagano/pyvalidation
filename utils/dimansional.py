import numpy as np

from pyvalidation.utils.config import UniqueIterable


def dimensional_count(value: UniqueIterable) -> int:
    """
    ## Summary:
        Recursively determine the dimensionality of a list.
    Arguments:
        value (tuple | list | np.ndarray | pd.Series):
            The list to be measured.
    Returns:
        int: The dimensionality of the list.
            - 0: The value is not a list. (str, int, float, etc.)
            - 1: The value is a list.
            - 2: The value is a list of lists.
            - 3: The value is a list of lists of lists.
            - ...
    Examples:
        >>> dimensional_measurement(1)
        0
        >>> dimensional_measurement('a')
        0
        >>> dimensional_measurement([1, 2, 3])
        1
        >>> dimensional_measurement([[1, 2, 3], [4, 5, 6]])
        2
        >>> dimensional_measurement([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
        3
    """
    if isinstance(value, UniqueIterable):
        try:
            value = value.tolist()
        except:
            try:
                value = value.tolist()
            except:
                pass
        return 1 + max(dimensional_count(item) for item in value) if value else 1
    else:
        return 0