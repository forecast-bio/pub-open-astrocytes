"""TODO"""

##
# Imports

import astrocytes

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
            _vprint( 'Snagging correct movie...' )
            started_movie = True
            recording_frames.append( frame )
        else:
            if started_movie:
                # We've moved to a new movie uuid, and so finished up
                _vprint( 'Got it!' )
                break
    
    return recording_frames

def movie_times( fs: list[BathApplicationFrame] ) -> NDArray:
    """TODO - Pull out the correct time interpretation from individual frames"""
    ##

    # TODO There is a bug at present in the `toile` export from the bath app.
    # data due to a glitch in the underlying raw recordings' time metadata;
    # for the time being pending re-export, we can compensate with a slight
    # kludge
    dt = fs[3].t

    ret = np.zeros( (len( fs ),) )
    for i, f in enumerate( fs ):
        ret[i] = 




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


#