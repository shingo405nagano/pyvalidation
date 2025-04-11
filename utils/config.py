import string
from typing import Union

import numpy as np
import pandas as pd

# HEX color patten type.
HEX_PATTERN = string.hexdigits + "#"

# Numeric type.
Numeric = Union[int, float]

# Numeric iterable type.
UniqueIterable = Union[tuple, list, np.ndarray, pd.Series]