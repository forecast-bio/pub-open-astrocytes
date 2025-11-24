"""Statistical analysis utilities including normalization and bootstrapping."""

##
# Imports

from tqdm import tqdm

import numpy as np

from numpy.random import RandomState
from numpy.typing import NDArray

from typing import (
    Callable,
)


##
# Helpers

def baseline_normalize( ts: NDArray, ys: NDArray,
            window: tuple[float, float]
        ):
    """Normalize signal using baseline statistics from a specified time window.

    Performs z-score normalization: (y - baseline_mean) / baseline_std

    Parameters
    ----------
    ts : NDArray
        Time values corresponding to signal samples
    ys : NDArray
        Signal values to normalize
    window : tuple[float, float]
        Time window [start, end) for computing baseline statistics

    Returns
    -------
    tuple[NDArray, float, float]
        Normalized signal, baseline mean, and baseline standard deviation
    """
    ##

    filter_cur = (
        (ts >= window[0])
        & (ts < window[1])
    )
    mean = np.mean( ys[filter_cur] )
    std = np.std( ys[filter_cur] )
    return (ys - mean) / std, mean, std


def _boot_traces_single( Xs: NDArray,
            axis: int = 0,
            rng: RandomState | None = None ) -> NDArray:
    """Generate a single bootstrap resample along specified axis.

    Parameters
    ----------
    Xs : NDArray
        Data array to resample
    axis : int, default=0
        Axis along which to resample
    rng : RandomState or None, default=None
        Random number generator; creates new one if None

    Returns
    -------
    NDArray
        Resampled array with same shape as input
    """
    ##

    if rng is None:
        rng = RandomState()
    sample_idx = rng.randint( Xs.shape[axis], size = (Xs.shape[axis]) )
    return Xs[sample_idx, :]

def boot_traces( Xs: NDArray,
            n: int = 200,
            axis: int = 0,
            rng: RandomState | None = None,
            verbose: bool = False
        ) -> NDArray:
    """Generate multiple bootstrap resamples of trace data.

    Parameters
    ----------
    Xs : NDArray
        Data array to resample
    n : int, default=200
        Number of bootstrap resamples to generate
    axis : int, default=0
        Axis along which to resample
    rng : RandomState or None, default=None
        Random number generator; creates new one if None
    verbose : bool, default=False
        Whether to show progress bar

    Returns
    -------
    NDArray
        Array of shape (n,) + Xs.shape containing bootstrap resamples
    """
    ##

    if rng is None:
        rng = RandomState()
    
    ret = np.zeros( (n,) + Xs.shape )
    it = tqdm( range( n ) ) if verbose else range( n )

    for i in it:
        ret[i] = _boot_traces_single( Xs,
            axis = axis,
            rng = rng,
        )
    return ret

def boot_stat( Xs: NDArray, f: Callable[[NDArray], NDArray],
            n: int = 200,
            axis: int = 0,
            rng: RandomState | None = None,
            verbose: bool = False
        ) -> NDArray:
    """Compute a statistic on bootstrap resamples for confidence estimation.

    Parameters
    ----------
    Xs : NDArray
        Data array to resample
    f : Callable[[NDArray], NDArray]
        Function that computes the statistic of interest on resampled data
    n : int, default=200
        Number of bootstrap resamples to generate
    axis : int, default=0
        Axis along which to resample
    rng : RandomState or None, default=None
        Random number generator; creates new one if None
    verbose : bool, default=False
        Whether to show progress bar

    Returns
    -------
    NDArray
        Array of computed statistics for each bootstrap resample
    """
    ##

    if rng is None:
        rng = RandomState()

    it = tqdm( range( n ) ) if verbose else range( n )
    
    boot_stats = np.array( [
        f( _boot_traces_single( Xs,
            axis = axis,
            rng = rng,
        ) )
        for _ in it
    ] )
    return boot_stats

#