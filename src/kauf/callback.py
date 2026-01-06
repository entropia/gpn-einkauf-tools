from .format.log import log_debug
from .settings import global_settings, DebugLevel


def callback(verbose: bool = False):
    if verbose:
        global_settings.debug_level = DebugLevel.DEBUG
        log_debug("verbose logging enabled")
