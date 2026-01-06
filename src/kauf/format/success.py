from rich import print
from rich.panel import Panel


def msg_success(msg: str):
    formatted_msg = f"[bold green]{msg}[/bold green]"
    print(
        Panel.fit(
            formatted_msg,
            title="Success",
            title_align="left",
            style="green",
        )
    )
