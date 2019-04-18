from ._version import get_versions
from .app import create_app

__all__ = ["create_app"]
__version__ = get_versions()["version"]
del get_versions
