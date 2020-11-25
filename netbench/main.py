"""
Entry point of the application.
"""

import click

from netbench.config import load_config, Config


@click.group()
@click.pass_context
def netbench(ctx: click.Context):
    """Main command of the application."""

    ctx.obj = load_config()


@netbench.command()
@click.pass_obj
@click.argument('key', type=str)
@click.argument('value', type=str)
def config(config: Config, key: str, value: str):
    """Change the configuration."""

    config.update(key, value)
