"""A (kind of) RESTful interface to Landlab graphs."""

from ._version import __version__
from .app import create_app

__all__ = ["__version__", "create_app"]
