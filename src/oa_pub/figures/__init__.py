"""TODO"""

##
# Imports

from forecast_style import HouseStyle

import matplotlib.pyplot as plt

from numpy.typing import NDArray
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.axes3d import Axes3D


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


def plot_trace_grid( axs, xs: NDArray, ys: list[list[NDArray]],
            color: str = '',
            xticks: list[float] | None = None,
            yticks: list[float] | None = None,
            ylim: tuple[float, float] | None = None,
            highlight: list[tuple[int, int]] = [],
        ):
    """TODO"""

    n_y = len( ys )
    n_x = len( ys[0] )

    for i in range( n_y ):
        for j in range( n_x ):
            ax = axs[i, j]
            cur_ys = ys[i][j]

            #

            ax.plot( xs, cur_ys, f'{color}-',
                linewidth = 1.5,
            )
            
            xl = ax.get_xlim()
            if ylim is None:
                cur_ylim = ax.get_ylim()
            else:
                cur_ylim = ylim
            
            ax.plot( xl, [0, 0],
                'k-',
                linewidth = 1,
                zorder = -200,
            )
            ax.fill_between( [0, xl[1]], cur_ylim[0], cur_ylim[1],
                color = 'k',
                alpha = 0.05,
                linewidth = 0,
                zorder = 100,
            )

            if (i, j) in highlight:
                ax.fill_between( [xl[0], xl[1]], cur_ylim[0], cur_ylim[1],
                    facecolor = 'none',
                    edgecolor = f'k',
                    alpha = 0.7,
                    linewidth = 2.,
                    zorder = -300,
                )
            
            ax.set_xlim( xl )
            ax.set_ylim( cur_ylim )

            ax.set_yticks( [] )
            ax.set_xticks( [] )
    
    if xticks is not None:
        # Add axis labels to only bottom-left
        for i in range( 1, n_x ):
            axs[-1, i].set_xticks( xticks, ['' for _ in xticks] )
        axs[-1, 0].set_xticks( xticks, [f'{x:+0.0f}' if x != 0 else '0' for x in xticks],
            fontsize = 11,
            rotation = 90,
        )

    if yticks is not None:
        axs[-1, 0].set_yticks( yticks, [f'{y:+0.0f}' if y != 0 else '0' for y in yticks],
            fontsize = 11,
        )


def plot_trajectory_3d( ax: Axes3D, vals: NDArray,
            color: str = '',
        ):
    """TODO"""

    # Start dot
    ax.scatter( vals[0, 0], vals[1, 0], vals[2, 0],
        color = 'k',
        s = 3
    )

    # End dot
    ax.scatter( vals[0, -1], vals[1, -1], vals[2, -1],
        facecolor = color,
        edgecolor = 'k',
        linewidth = 0.5,
        s = 8
    )

    # Trajectory
    ax.plot( vals[0, :], vals[1, :], vals[2, :],
        f'{color}-',
        linewidth = 0.5,
        alpha = 0.8,
    )


#