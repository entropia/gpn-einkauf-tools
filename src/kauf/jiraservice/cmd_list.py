from typing import Optional

import typer
import keyring
from typing_extensions import Annotated

from kauf.format.shopping_list import ShoppingList
from kauf.hedgedocservice.service import HedgeDocService
from kauf.jiraservice import log_debug, msg_success
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
    tag: Annotated[Optional[str], typer.Option(help="Tag to list items for.")] = None,
    status_exclude: Annotated[
        list[str], typer.Option(help="List of statuses to exclude.")
    ] = [],
    keys: Annotated[
        list[str], typer.Option("--keys", "-k", help="List of issue keys to filter for.")
    ] = [],
):
    token = keyring.get_password(KAUF_KEYRING_SERVICENAME, "jira_token")
    if not token:
        msg_error("Missing JIRA token.", command_alt="kauf secrets set jira_token XXX")
    if not tag and len(keys) == 0:
        msg_error("Missing tag or keys.")

    sid_cookie = keyring.get_password(KAUF_KEYRING_SERVICENAME, "hedgedoc_sid")

    j = JIRAService(token, jira_url)
    issues = j.search_issues("EINKAUF", [tag] if tag else [], status_exclude=status_exclude, keys=keys)

    if len(issues) == 0:
        msg_error("0 issues found.")

    log_debug(f"{len(issues)} issues selected")

    h = HedgeDocService(hedgedoc_url, sid_cookie=sid_cookie)
    shopping_list = ShoppingList(issues, jira_url)

    if len(hedgedoc_url) > 0:
        url = h.new_pad(shopping_list.as_markdown())
        msg_success(f"Created HedgeDoc at\n{url}")
    else:
        log_debug("no HedgeDoc URL provided, printing to stdout")
        print(shopping_list.as_markdown())
