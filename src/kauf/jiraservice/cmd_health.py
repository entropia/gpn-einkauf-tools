import typer
import keyring
from typing_extensions import Annotated

from kauf.format.success import msg_success
from .service import JIRAService

from ..format import msg_error
from ..secrets import KAUF_KEYRING_SERVICENAME

jira_app = typer.Typer()


@jira_app.command("health")
def health(
    jira_url: Annotated[
        str, typer.Option(help="Base URL of the JIRA instance to use.")
    ] = "",
):
    token = keyring.get_password(KAUF_KEYRING_SERVICENAME, "jira_token")
    if not token:
        msg_error("Missing JIRA token.", command_alt="kauf secrets set jira_token XXX")

    j = JIRAService(token, jira_url)
    if len(j.get_projects()) == 0:
        msg_error("No access to any JIRA project")

    msg_success("Token is working and having access to at least 1 project.")
