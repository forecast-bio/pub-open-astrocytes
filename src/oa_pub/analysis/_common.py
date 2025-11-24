"""Common helper functions for analysis operations."""

##
# Imports

from numpy.typing import NDArray


##
# Helpers

def is_between( xs: NDArray, window: tuple[float, float] ) -> NDArray:
    """Check if values fall within a specified window.

    Parameters
    ----------
    xs : NDArray
        Array of values to check
    window : tuple[float, float]
        Lower and upper bounds (inclusive lower, exclusive upper)

    Returns
    -------
    NDArray
        Boolean array where True indicates values within [window[0], window[1])
    """
    return (
        (xs >= window[0])
        & (xs < window[1])
    )

#