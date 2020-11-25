"""
Custom click types.
"""

import socket

import click


class IPaddress(click.ParamType):
    """An IPv4 address."""

    name = 'IP'

    def convert(self, value, param, ctx):
        try:
            socket.inet_aton(value)
            return value
        except socket.error:
            self.fail(f'{value!r} is not a valid IP address.', param, ctx)
