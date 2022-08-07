import importlib
import logging
import os

from .default_settings import *  # pull in all default settings


class Environments:
    LOCAL = "local"
    PRODUCTION = "production"


ENV = os.environ.get("ENV", Environments.LOCAL)


def is_production() -> bool:
    """Check if current environment is production"""
    return ENV == Environments.PRODUCTION


def is_local() -> bool:
    """Check if current environment is local"""
    return ENV == Environments.LOCAL


_logger = logging.getLogger(__name__)

# pull in the settings from the correct environment
try:
    mod = importlib.import_module(f"{__name__}.{ENV}_settings")
    for key in dir(mod):
        if key.isupper():
            globals()[key] = mod.__dict__[key]
except ImportError:
    _logger.info(f"Settings file for {ENV} environment not found, using defaults!")


# clean up the exports so that they don't appear in exports
del os
del logging
del importlib
