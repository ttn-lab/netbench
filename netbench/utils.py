"""
Applicaton-wide utilities.
"""

import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd


def write_results(results: pd.DataFrame, path: str, *args):
    """
    Write test results to a CSV file.

    The given path must be a folder in which the file will be stored. If the
    folder doesn't exist, it will be created.
    """

    Path(path).mkdir(parents=True, exist_ok=True)
    output_file = os.path.join(
        path,
        f'{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}_{"-".join(args)}.csv')
    results.to_csv(output_file, index_label='iter')
    print(f'Results written to {output_file}')
