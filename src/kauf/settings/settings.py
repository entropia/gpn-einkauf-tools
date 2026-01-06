from enum import StrEnum


class DebugLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"


class Settings:
    debug_level = DebugLevel.INFO


# Initiated immediately here so it can be manipulated by typer callbacks.
global_settings = Settings()
