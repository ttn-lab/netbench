"""
Entry point of the application. 
"""

import click

from netbench.bandwidth import bandwidth
from netbench.config import Config, load_config
from netbench.latency import latency
from netbench.ptp import ptp


@click.group()
@click.pass_context
def netbench(ctx: click.Context):
    """CLI utility that wraps many network benchmarks for ease of use."""

    ctx.obj = load_config()


@netbench.command()
@click.pass_obj
@click.argument('key', type=str)
@click.argument('value', type=str)
def config(config: Config, key: str, value: str):
    """Change the configuration."""

    config.update(key, value)


netbench.add_command(bandwidth)
netbench.add_command(ptp)
netbench.add_command(latency)
