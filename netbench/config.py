"""
Application configuration logic.
"""

import json
import os
from pathlib import Path

config_file = f'{os.environ["HOME"]}/.config/netbench/config.json'


class Config():
    """App configuration."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def update(self, key: str, value: str):
        """
        Update the app's configuration.

        Set a new value for the given key. If the key didn't exist in the
        configuration before, it will be created.
        """

        self.__dict__.update({key: value})
        with open(config_file, 'w') as f:
            json.dump(self.__dict__, f)


def load_config() -> Config:
    """
    Load the app's configuration from file.

    If a configuration file is not found, a default one will be created.
    """

    try:
        with open(config_file, 'r') as f:
            values = json.load(f)
    except FileNotFoundError:
        values = create_default_config()
    return Config(**values)


def create_default_config() -> dict:
    """Create a configuration file with default values."""

    default_values = {
        'results_path': f'{os.environ["HOME"]}/netbench'
    }
    Path(os.path.dirname(config_file)).mkdir(parents=True, exist_ok=True)
    with open(config_file, 'w') as f:
        json.dump(default_values, f)
    return default_values
