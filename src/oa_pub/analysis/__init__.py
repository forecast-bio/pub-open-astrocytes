"""Analysis tools for astrocyte calcium imaging and embedding data.

This module provides utilities for:
- Loading bath application recordings and patch embeddings
- Statistical analysis including baseline normalization and bootstrapping
- Time window filtering and data extraction
"""

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
# Expose exports

from ._constants import (
    N_PATCHES_X,
    N_PATCHES_Y,
    #
    COMPOUND_ALIASES,
)

from ._common import (
    is_between,
)

from ._extraction import (
    get_movie,
    get_movie_traces,
    movie_times,
)

from ._stats import (
    baseline_normalize,
    #
    boot_traces,
    boot_stat,
)


#