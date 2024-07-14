import numpy as np


def mpl_calc_series(n_groups, n_bars, group_width, bar_width, bar_gap):
    # IMPORTANT: This algorithm only produces correct bar widths when the
    # figure's width is determined exclusively by the n_groups given.
    # When you combine the plot with other elements that change the x-axis
    # limits, the bars will be rescaled and have an incorrect width.
    bar_gap *= n_groups
    bar_width *= n_groups
    min_bar_gap = min(bar_gap, 0.03)
    min_width = bar_width * n_bars + min_bar_gap * (n_bars - 1)
    if min_width > group_width:
        algorithm = mpl_calc_scaled_group_series
        bar_width = mpl_calc_bar_width(n_bars, group_width)
    else:
        if bar_width * n_bars + bar_gap * (n_bars - 1) > group_width:
            bar_gap = (group_width - n_bars * bar_width) / (n_bars - 1)
        algorithm = mpl_calc_clustered_group_series
    group_points = algorithm(n_bars, group_width, bar_width, bar_gap)
    return bar_width, [i + group_points for i in range(n_groups)]


def mpl_calc_scaled_group_series(n_bars, group_width, bar_width, bar_gap):
    width = max(1, n_bars - 1)
    half_width = width / 2
    centered = np.arange(n_bars) - half_width
    bar_width = mpl_calc_bar_width(n_bars, group_width)
    return centered / width * (group_width - bar_width)


def mpl_calc_clustered_group_series(n_bars, group_width, bar_width, bar_gap):
    hop = bar_width + bar_gap
    return np.array([hop * i - (hop * (n_bars - 1)) / 2 for i in range(n_bars)])


def mpl_calc_bar_width(n_bars, group_width):
    estimate = (group_width - 0.03 * n_bars) / n_bars
    for i in range(50):
        estimate = ((group_width - estimate) - 0.03 * n_bars) / n_bars
    return estimate
