import typer
import keyring
from typing_extensions import Annotated

from kauf.format.shopping_list import ShoppingList
from kauf.hedgedocservice.service import HedgeDocService
from kauf.jiraservice import msg_success
from .service import JIRAService

from ..format import msg_error
from ..secrets import KAUF_KEYRING_SERVICENAME
from .cmd_health import jira_app
from rich import print


@jira_app.command("list")
def list(
    jira_url: Annotated[
        str, typer.Option(help="Base URL of the JIRA instance to use.")
    ] = "",
    hedgedoc_url: Annotated[
        str, typer.Option(help="Base URL of the HedgeDoc instance to use.")
    ] = "",
    tag: Annotated[str, typer.Option(help="Tag to list items for.")] = "",
):
    token = keyring.get_password(KAUF_KEYRING_SERVICENAME, "jira_token")
    if not token:
        msg_error("Missing JIRA token.", command_alt="kauf secrets set jira_token XXX")
    if not tag:
        msg_error("Missing tag.")

    j = JIRAService(token, jira_url)
    issues = j.search_issues("EINKAUF", [tag])

    h = HedgeDocService(hedgedoc_url)
    shopping_list = ShoppingList(issues, jira_url)

    url = h.new_pad(shopping_list.as_markdown())

    msg_success(url)
