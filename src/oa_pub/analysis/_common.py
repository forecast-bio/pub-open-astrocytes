"""TODO"""

##
# Imports

from numpy.typing import NDArray


##
# Helpers

def is_between( xs: NDArray, window: tuple[float, float] ) -> NDArray:
    """TODO"""
    return (
        (xs >= window[0])
        & (xs < window[1])
    )

#