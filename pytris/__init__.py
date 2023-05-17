"""
pyTRIS
------

pyTRIS - a simple API wrapper for Highways England's WebTRIS Traffic Flow API.
"""

import logging

from .api import API
from . import models


__all__ = ['API']

# Set up logging
logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s: %(name)s (%(levelname)s) %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)


def enable_debug_mode():
    """Utility function for enabling more detailed log messages
    """
    logger.setLevel(logging.DEBUG)


def disable_logs():
    """Utility function for entirely disabling log messages. 
    """
    logger.setLevel(logging.WARNING)
