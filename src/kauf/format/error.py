from rich import print
from rich.panel import Panel
import typer


def msg_error(msg: str, command_alt: str = None):
    formatted_msg = f"[bold red]{msg}[/bold red]"
    if command_alt:
        formatted_msg += (
            f"\n[bright_black]Try: [italic]{command_alt}[/bright_black][/italic]"
        )
    print(
        Panel.fit(
            formatted_msg,
            title="Error",
            title_align="left",
            style="red",
        )
    )

    raise typer.Exit(1)
