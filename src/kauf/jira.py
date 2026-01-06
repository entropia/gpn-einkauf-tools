import typer
import keyring
from typing_extensions import Annotated

from .format import msg_error
from .secrets import KAUF_KEYRING_SERVICENAME

jira_app = typer.Typer()


@jira_app.command("health")
def health(
    jira_url: Annotated[
        str, typer.Argument(help="Base URL of the JIRA instance to use.")
    ] = "",
):
    token = keyring.get_password(KAUF_KEYRING_SERVICENAME, "jira_token")
    if not token:
        msg_error("Missing JIRA token.", command_alt="kauf secrets set jira_token XXX")
    pass
