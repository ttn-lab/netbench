"""
Command for Latency testing.
"""

import os
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

    output_file_name = "/output.txt"
    path = os.path.join(config.results_path, 'latency')
    Path(path).mkdir(parents=True, exist_ok=True)

    print('Starting ping benchmark.')
    # ping(server_addr, verbose=True, timeout=t, payload=p)
    call('ping ' + server_addr + ' -w ' + str(t) + ' -s ' + str(s) +
         ' > ' + path + output_file_name, shell=True)

    f = open(path + output_file_name, "r")

    sync = False
    latency = []

    for line in f:
        if("ttl" in line):
            sync = True
            line_vect = line.replace('=', ' ')
            line_vect = line_vect.split(' ')
            latency_index = line_vect.index("time")
            latency.append(line_vect[latency_index + 1])

    if(sync):
        print("\nResume: " + line)
        print('Benchmark finished, saving results in ' +
              path + '.')

        df = pd.DataFrame(columns=['latency'])

        for h in range(len(latency)):
            df = df.append(pd.DataFrame({
                'latency': pd.Series([latency[h]], dtype='float')
            }), ignore_index=True)

        write_results(
            df,
            os.path.join(config.results_path, 'latency'),
            'ping'
        )

    else:
        print(server_addr + " unreachable.")
