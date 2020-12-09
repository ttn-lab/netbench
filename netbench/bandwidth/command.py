"""
Command for bandwidth testing.
"""

import json
import os
import random
from subprocess import call

import click
import pandas as pd
from netbench.config import Config
from netbench.types import IPaddress
from netbench.utils import write_results


@click.command()
@click.pass_obj
@click.option('-t', default=10, show_default=True, help='Duration of the benchmark in seconds')
@click.option('-s', default=1, show_default=True, help='Number of streams to use.')
@click.option('-u', default=False, is_flag=True, help='Use UDP instead of TCP.')
@click.argument('server_addr', type=IPaddress())
def bandwidth(config: Config, server_addr: str, t: int, s: int, u: bool):
    """
    Bandwidth benchmarking using iperf3.

    The remote server's IP address must be specified.
    """

    print('Starting iperf3 benchmark.')
    output_file = f'/tmp/iperf-test-{random.randint(0, 10000)}.json'
    call(f'iperf3 -c {server_addr} {"-u" if u else ""} -t {t} -P {s}' +
         f' -J > {output_file}', shell=True)

    print('Benchmark finished, saving results.')
    df = pd.DataFrame(columns=['bytes', 'seconds', 'bits_per_second'])
    with open(output_file, 'r') as output:
        results = json.load(output)
        for interval in results['intervals']:
            df = df.append(pd.DataFrame({
                'bytes': pd.Series([interval['sum']['bytes']], dtype='int'),
                'seconds': pd.Series([interval['sum']['seconds']], dtype='float'),
                'bits_per_second': pd.Series([interval['sum']['bits_per_second']], dtype='float')
            }), ignore_index=True)

    write_results(
        df,
        os.path.join(config.results_path, 'bandwidth'),
        'udp' if u else 'tcp',
        f'{s}streams'
    )
