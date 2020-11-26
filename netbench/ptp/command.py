"""
Command for PTP testing.
"""

import os

import click
import pandas as pd
from subprocess import call
from netbench.config import Config
from netbench.types import IPaddress
from netbench.utils import write_results
from pathlib import Path


@click.command()
@click.pass_obj
@click.option('-t', default=10, show_default=True, help='Duration of the benchmark in seconds')
@click.option('-s', default=False, is_flag=True, help='Force slave mode.')
@click.argument('interface')
def ptp(config: Config, interface: str, t: int, s: bool):
    """
    PTP benchmarking using ptp4l.

    The PTP enabled interface must be specified.
    """

    slave_mode = '-s' if s else ''
    path = os.path.join(config.results_path, 'ptp')

    Path(path).mkdir(parents=True, exist_ok=True)

    print('Starting PTP benchmark.')
    call('sudo timeout ' + str(t) + ' ptp4l -i ' +
         interface + ' -m ' + slave_mode + ' > ' + path + '/output.txt', shell=True)

    print('Benchmark finished, saving results.')
