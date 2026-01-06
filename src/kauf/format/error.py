from rich import print
from rich.panel import Panel


def msg_error(msg: str, command_alt: str = None):
    print(
        Panel.fit(
            f"[bold red]{msg}[/bold red]\n[bright_black]Try: [italic]{command_alt}[/bright_black][/italic]",
            title="Error",
            title_align="left",
            style="red",
        )
    )
