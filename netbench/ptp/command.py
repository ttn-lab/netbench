"""
Command for PTP testing.
"""

import os

import click
import pandas as pd
from statistics import mean, median, stdev
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

    output_file_name = "/output.txt"
    path = os.path.join(config.results_path, 'ptp')
    Path(path).mkdir(parents=True, exist_ok=True)

    print('Starting PTP benchmark.')
    call('sudo timeout ' + str(t) + ' ptp4l -i ' +
         interface + ' -m ' + slave_mode + ' > ' + path + output_file_name, shell=True)

    f = open(path + output_file_name, "r")

    sync = False
    offset = []
    freq = []
    delay = []
    state = []

    for line in f:
        if("offset" in line):
            sync = True
            line_vect = line.split(' ')
            line_vect = [x for x in line_vect if x != '']
            offset_index = line_vect.index("offset")
            offset.append(line_vect[offset_index + 1])
            state.append(line_vect[offset_index + 2])
            freq_index = line_vect.index("freq")
            freq.append(line_vect[freq_index + 1])
            delay_index = line_vect.index("delay")
            delay.append(line_vect[delay_index + 1]
                         [0:len(line_vect[delay_index + 1])-1])

    if(sync):
        offset_s2 = [(float(offset[x]))
                     for x in range(len(state)) if state[x] == "s2"]
        freq_s2 = [float(freq[x])
                   for x in range(len(state)) if state[x] == "s2"]
        delay_s2 = [float(delay[x])
                    for x in range(len(state)) if state[x] == "s2"]

        df = pd.DataFrame(columns=['offset', 'freq', 'delay', 'state'])

        for h in range(len(state)):
            df = df.append(pd.DataFrame({
                'offset': pd.Series([offset[h]], dtype='float'),
                'freq': pd.Series([freq[h]], dtype='float'),
                'delay': pd.Series([delay[h]], dtype='float'),
                'state': pd.Series([state[h]], dtype='string')
            }), ignore_index=True)

        write_results(
            df,
            os.path.join(config.results_path, 'ptp'),
            'ptp'
        )

        offset_mean = mean(offset_s2)
        offset_median = median(offset_s2)
        freq_mean = mean(freq_s2)
        freq_median = median(freq_s2)
        delay_mean = mean(delay_s2)
        delay_median = median(delay_s2)

        print("Number of available measurements: %d." % (len(offset)))
        print("The offset mean is: %f nanoseconds." % (offset_mean))
        print("The offset median is: %f nanoseconds." % (offset_median))
        print("The frequency adjustment std is: %d ppm." % (stdev((freq_s2))))
        print("The maximum frequency adjustment is: %d ppm." % (max((freq_s2))))
        print("The minimum frequency adjustment is: %d ppm." % (min(freq_s2)))
        print("The frequency adjustment mean is: %d ppm." % (freq_mean))
        print("The frequency adjustment median is: %d ppm." % (freq_median))
        print("The delay mean is: %d ns." % (delay_mean))
        print("The delay median is: %d ns." % (delay_median))

        print('Benchmark finished, saving results in ' +
              path + '.')

    else:
        print("Not PTP synchronization available on the interface " + interface + ".")
