"""TODO"""

##
# Imports

import atdata
import astrocytes

from astrocytes._datasets._embeddings import PatchEmbeddingTrace
from astrocytes.schema import BathApplicationFrame

import numpy as np
from numpy.typing import NDArray


##
# Constants

N_PATCHES_Y = 14
N_PATCHES_X = 14


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


#