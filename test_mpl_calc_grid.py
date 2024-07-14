import itertools
import math
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


def calc_series(n_groups, n_bars, group_width, bar_width, bar_gap):
    bar_gap *= n_groups
    bar_width *= n_groups
    min_bar_gap = min(bar_gap, 0.03)
    min_width = bar_width * n_bars + min_bar_gap * (n_bars - 1)
    if min_width > group_width:
        algorithm = calc_scaled_group_series
        bar_width = calc_bar_width(n_bars, group_width)
    else:
        if bar_width * n_bars + bar_gap * (n_bars - 1) > group_width:
            bar_gap = (group_width - n_bars * bar_width) / (n_bars - 1)
        algorithm = calc_clustered_group_series
    group_points = algorithm(n_bars, group_width, bar_width, bar_gap)
    return bar_width, [i + group_points for i in range(n_groups)]


def calc_scaled_group_series(n_bars, group_width, bar_width, bar_gap):
    width = max(1, n_bars - 1)
    half_width = width / 2
    centered = np.arange(n_bars) - half_width
    bar_width = calc_bar_width(n_bars, group_width)
    return centered / width * (group_width - bar_width)

def calc_clustered_group_series(n_bars, group_width, bar_width, bar_gap):
    hop = bar_width + bar_gap
    return np.array([hop * i - (hop * (n_bars - 1)) / 2 for i in range(n_bars)])


def calc_bar_width(n_bars, group_width):
    est = (group_width - 0.03 * n_bars) / n_bars
    for i in range(50):
        est = ((group_width - est) - 0.03 * n_bars) / n_bars
    return est


def plot_series(g, bpg, ax: Axes = None):
    show = False
    if ax is None:
        fig, ax = plt.subplots()
        show = True
    group_width = 0.5
    bar_gap = 0.03
    bar_width = 0.03
    bar_width, point_series = calc_series(g, bpg, group_width=group_width, bar_width=bar_width, bar_gap=bar_gap)
    points = [*itertools.chain.from_iterable(point_series)]
    ax.boxplot([np.random.rand(50) for _ in points], positions=points, widths=bar_width)
    if show:
        plt.show()


max_groups = 9
max_bar_per_group = 4

fig, ax_grid = plt.subplots(max_groups, max_bar_per_group)
for g, ax_row in zip(range(1, max_groups + 1), ax_grid):
    for bpg, ax in zip(range(1, max_bar_per_group + 1), ax_row):
        plot_series(g, bpg, ax)

plt.show()
