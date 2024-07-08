"""
Automize Science is a Python package designed to elaborate data into graphs coming from lipid extractions (LC/MS).
Starting from a file containing the **pmol/mg** values per each sample, this package streamlines the process of data
analysis and visualization.
"""

from .graph_constructor import *
from .workflows import data_workflow

__version__ = "1.0.2"
