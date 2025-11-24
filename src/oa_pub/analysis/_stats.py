"""TODO"""

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
    """TODO"""
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
    """TODO"""
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
    """TODO"""
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
    """TODO"""
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