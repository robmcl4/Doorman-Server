"""
  config.py

  Read the config from 'config.cfg' in the same directory as this
  file. Then store that config as a dict in 'config.config'

  Expected config.cfg structure:
  [mysql]: user, pass, host, port, database

  Author: Robert McLaughlin
"""

from configparser import SafeConfigParser
import os
import logging

logger = logging.getLogger(__name__)

_path = os.path.dirname(os.path.abspath(__file__))
_config_path = os.path.join(_path, "config.cfg")

config = None

def read_config():
    """
        Read from config.cfg and load it as a dict
        store the dict into the package-global config variable
    """
    global config
    parser = SafeConfigParser()
    parser.read(_config_path)
    config = parser

read_config()
