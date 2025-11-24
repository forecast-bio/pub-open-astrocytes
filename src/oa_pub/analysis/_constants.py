"""TODO"""

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
