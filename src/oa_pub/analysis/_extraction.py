"""Data extraction utilities for loading astrocyte recordings and embeddings."""

##
# Imports

import atdata
import astrocytes

import numpy as np

#

from astrocytes.schema import BathApplicationFrame
from astrocytes._datasets._embeddings import PatchEmbeddingTrace

from numpy.typing import NDArray

#

from oa_pub.analysis._constants import (
    N_PATCHES_X,
    N_PATCHES_Y,
)


##
# Helpers

def get_movie(
            movie_uuid: str,
            verbose: bool = False
        ) -> list[BathApplicationFrame]:
    """Load all frames for a specific recording from the bath application dataset.

    Parameters
    ----------
    movie_uuid : str
        Unique identifier for the recording
    verbose : bool, default=False
        Whether to print progress messages

    Returns
    -------
    list[BathApplicationFrame]
        All frames belonging to the specified recording, in temporal order
    """

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
    """Load all patch embedding traces for a specific recording.

    Retrieves DINOv3 vision transformer patch embeddings for each frame of a
    recording, organized spatially as a 14×14 grid.

    Parameters
    ----------
    movie_uuid : str
        Unique identifier for the recording
    verbose : bool, default=False
        Whether to print progress messages

    Returns
    -------
    list[list[PatchEmbeddingTrace]]
        2D list of shape (N_PATCHES_Y, N_PATCHES_X) containing embedding traces
        for each spatial patch location
    """

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
    """Extract time array and frame interval from a list of recording frames.

    Parameters
    ----------
    fs : list[BathApplicationFrame]
        Frames from a recording, in temporal order

    Returns
    -------
    tuple[NDArray, float]
        Time array (in seconds) for each frame, and the time interval (dt) between frames

    Notes
    -----
    There is a known bug in the toile export from the bath application dataset
    that affects time metadata. This function compensates by reconstructing times
    from the frame interval.
    """
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

#