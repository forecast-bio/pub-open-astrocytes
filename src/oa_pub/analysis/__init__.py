"""TODO"""

##
# Imports

from tqdm import tqdm

import atdata
import astrocytes

# TODO pending additional typing for trace classes
# => see https://github.com/forecast-bio/open-astrocytes/issues/15
from astrocytes._datasets._embeddings import PatchEmbeddingTrace
from astrocytes.schema import BathApplicationFrame

import numpy as np

from numpy.typing import NDArray
from numpy.random import RandomState
from typing import (
    Callable,
)


##
# Constants

N_PATCHES_Y = 14
"Number of patches in the y-dimension for the embedding model"
N_PATCHES_X = 14
"Number of patches in the x-dimension for the embedding model"

# TODO pending additional typing for trace classes
# => see https://github.com/forecast-bio/open-astrocytes/issues/15
COMPOUND_ALIASES = {
    'baclofen': [
        'baclofen',
        'bacloffen',
    ],
    'tacpd': [
        'tacpd',
    ]
}
"""Different spelling variants used to indicate each applied compound

There were some typos in the raw metadata for the bath-app dataset; these are
corrected for in the `Frame` sample schemas but not for the embedding and trace
ones yet, as they don't have explicit metadata types yet)
"""


##
# Helpers

def get_movie(
            movie_uuid: str,
            verbose: bool = False
        ) -> list[BathApplicationFrame]:
    "TODO"

    def _vprint( *args, **kwargs ):
        if verbose:
            print( *args, **kwargs )

    #

    assert astrocytes.data.bath_application is not None, \
        "Unable to find backend manifest for 'bath_application'"

    ds = astrocytes.data.bath_application \
            .as_type( BathApplicationFrame )

    started_movie = False
    recording_frames = []
    _vprint( 'Iterating frames...' )
    for frame in ds.ordered( batch_size = None ):
        if frame.movie_uuid == movie_uuid:
            if not started_movie:
                _vprint( 'Snagging correct movie...' )
            started_movie = True
            recording_frames.append( frame )
        else:
            if started_movie:
                # We've moved to a new movie uuid, and so finished up
                _vprint( 'Got it!' )
                break
    
    return recording_frames


def get_movie_traces(
            movie_uuid: str,
            verbose: bool = False
        ) -> list[list[PatchEmbeddingTrace]]:
    "TODO Return all patch embedding traces for a given recording"

    def _vprint( *args, **kwargs ):
        if verbose: print( *args, **kwargs )

    # TODO Change over to `atdata`'s new `wids` indexed
    # WebDatasets for faster streaming  in demos
    wds_url = (
        'https://data.forecastbio.cloud'
        + '/testing/patch-pc-traces/bath-application/'
        + 'bath_app-dinov3_vit7b16-pca64-smooth84.tar'
    )
    ds = atdata.Dataset[PatchEmbeddingTrace]( wds_url )

    started_movie = False
    movie_traces: list[PatchEmbeddingTrace] = []

    _vprint( 'Iterating traces...' )
    for trace in ds.ordered( batch_size = None ):
        try:
            assert trace.metadata is not None
            assert 'uuid' in trace.metadata

            if trace.metadata['uuid'] == movie_uuid:
                _vprint( 'Snagging correct movie...' )
                started_movie = True
                movie_traces.append( trace )

            else:
                if started_movie:
                    # We've moved to a new movie uuid,
                    # and so are finished here
                    _vprint( 'Got it!' )
                    break
        except:
            # Skip trace - no metadata
            continue
    
    # Arrange result spatially
    ret: list[list[PatchEmbeddingTrace | None]] = [
        [
            None
            for j in range( N_PATCHES_X )
        ]
        for i in range( N_PATCHES_Y )
    ]

    for trace in movie_traces:
        assert trace.i_patch is not None and trace.j_patch is not None, \
            "Can't export in localized form without patch location metadata"
        ret[trace.i_patch][trace.j_patch] = trace

    # TODO We don't actually fully have assurance that ret type-checks here!
    # Will require just a slight re-think on logic
    return ret


def movie_times( fs: list[BathApplicationFrame] ) -> tuple[NDArray, float]:
    """TODO - Pull out the correct time interpretation from individual frames"""
    ##

    # TODO There is a bug at present in the `toile` export from the bath app.
    # data due to a glitch in the underlying raw recordings' time metadata;
    # for the time being pending re-export, we can compensate with a slight
    # kludge
    dt = fs[3].t

    ret = np.zeros( (len( fs ),) )
    for i, f in enumerate( fs ):
        # TODO Double-check if the 't_index' metadata also has the original off-by-one
        ret[i] = i * dt
    
    return ret, dt


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


def is_between( xs: NDArray, window: tuple[float, float] ) -> NDArray:
    """TODO"""
    return (
        (xs >= window[0])
        & (xs < window[1])
    )


##

def boot_sample_traces( Xs: NDArray,
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
        ret[i] = boot_sample_traces( Xs, axis = axis, rng = rng )
    return ret


def boot_stat( Xs: NDArray, f: Callable[[NDArray], NDArray],
            n: int = 200,
            axis: int = 0,
            rng: RandomState | None = None,
            verbose: bool = False
        ) -> NDArray:
    if rng is None:
        rng = RandomState()

    it = tqdm( range( n ) ) if verbose else range( n )
    
    boot_stats = np.array( [ f( boot_sample_traces( Xs, axis = axis, rng = rng ) )
                             for i in it ] )
    return boot_stats


#