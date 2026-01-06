import keyring
import typer
from typing import Annotated

from .jira import callback

KAUF_KEYRING_SERVICENAME = "KAUF"

secrets_app = typer.Typer(callback=callback)


@secrets_app.command("set")
def set_secret(
    name: Annotated[str, typer.Argument(help="Secret name.")] = "",
    value: Annotated[str, typer.Argument(help="Secret value.")] = "",
):
    keyring.set_password(KAUF_KEYRING_SERVICENAME, name, value)
