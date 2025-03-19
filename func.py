from typing import Iterable
import numpy as np
def flatten(lst: Iterable) -> Iterable:
    for item in lst:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)  # yields all sub-items
        else:
            yield item

def multilerp(v: np.ndarray, alpha: float):
    if len(v.shape) != 2:
        raise ValueError("Input must be a 2D matrix.")
    
    # Use divmod to get integer part and positive fractional part
    full, frac = divmod(alpha, 1)
    full = int(full)
    
    # Optional: Clamp indices to valid range to prevent out-of-bounds
    n = v.shape[0]
    full = np.clip(full, 0, n - 2)  # Ensures full+1 is within bounds
    
    # Linear interpolation between consecutive rows
    return (1 - frac) * v[full] + frac * v[full + 1]

