"""
Applicaton-wide utilities.
"""

import os
from datetime import datetime

import pandas as pd


def write_results(results: pd.DataFrame, path: str):
    """
    Write test results to a CSV file.

    The given path must be a folder in which the file will be stored. If the
    folder doesn't exist, it will be created.
    """

    results.to_csv(os.path.join(
        path, f'{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.csv'), index_label=False)
