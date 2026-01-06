from kauf.settings import DebugLevel, global_settings
from rich import print
from datetime import datetime


def log_debug(msg: str):
    if global_settings.debug_level != DebugLevel.DEBUG:
        return

    print(
        f"[bright_black][{datetime.now().strftime('%H:%M:%S')}]   {msg}[/bright_black]"
    )
