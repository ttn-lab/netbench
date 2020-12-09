"""
Command for Latency testing.
"""

import os
import random
from pathlib import Path
from subprocess import call

import click
import pandas as pd
from netbench.config import Config
from netbench.types import IPaddress
from netbench.utils import write_results


@click.command()
@click.pass_obj
@click.option('-t', default=10, show_default=True, help='Duration of the benchmark in seconds')
@click.option('-s', default=56, show_default=True, help='Size of the payload in bytes (+ 8 from the ICMP header)')
@click.argument('server_addr', type=IPaddress())
def latency(config: Config, server_addr: str, t: int, s: int):
    """
    Latency benchmarking using ping.

    The destination IP adress must be specified.
    """

    print('Starting ping benchmark.')
    output_file = f'/tmp/ping-test-{random.randint(0, 10000)}.txt'
    call(f'ping {server_addr} -w {str(t)} -s {str(s)}' +
         f' > {output_file}', shell=True)

    sync = False
    latency = []
    with open(output_file, 'r') as output:
        for line in output:
            if("ttl" in line):
                sync = True
                line_vect = line.replace('=', ' ')
                line_vect = line_vect.split(' ')
                latency_index = line_vect.index("time")
                latency.append(line_vect[latency_index + 1])

    if(sync):
        print(f'Resume: {line}')

        df = pd.DataFrame(columns=['latency'])
        for h in range(len(latency)):
            df = df.append(pd.DataFrame({
                'latency': pd.Series([latency[h]], dtype='float')
            }), ignore_index=True)

        print('Benchmark finished, saving results.')
        write_results(
            df,
            os.path.join(config.results_path, 'latency'),
            'ping'
        )
    else:
        print(f'{server_addr} unreachable.')
