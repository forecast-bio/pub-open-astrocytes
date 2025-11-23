"""TODO"""

##
# Imports

from forecast_style import HouseStyle

import matplotlib.pyplot as plt

from numpy.typing import NDArray
from matplotlib.axes import Axes


##
# Helpers

def plot_micrograph( s: HouseStyle, image: NDArray,
            ax: Axes | None = None,
            scale_x: float = 1.,
            scale_y: float = 1.,
            scale_bar: float = 100.,
            **kwargs
        ):
    """TODO"""
    
    if ax is None:
        ax = plt.gca()

    s.show_micrograph( ax, image,
        scale_x = scale_x,
        scale_y = scale_y,
        **kwargs
    )
    s.label(
        data_xlim = (0, scale_bar),
        data_ylim = None,
    )
    
    # Override some of the `HouseStyle` default behavior on ticks
    plt.xticks( [0, scale_bar], ['0', f'{scale_bar:0.0f} $\\mu$m'],
        ha = 'left'
    )
    plt.yticks( [] )


#