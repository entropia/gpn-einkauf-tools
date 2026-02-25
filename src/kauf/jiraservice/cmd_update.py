import typer
import keyring
import re
from typing_extensions import Annotated

from kauf.format import msg_error, log_debug, msg_success
from ..secrets import KAUF_KEYRING_SERVICENAME
from kauf.hedgedocservice.service import HedgeDocService
from .cmd_health import jira_app
from .service import JIRAService


@jira_app.command("update")
def update(
    jira_url: Annotated[
        str, typer.Option(help="Base URL of the JIRA instance to use.")
    ],
    hedgedoc_url: Annotated[
        str, typer.Option(help="URL pointing to an HedgeDoc document.")
    ],
    transition: Annotated[
        str, typer.Option(help="Name of the transition to update issues with.")
    ],
):
    # Part 1: extract finished items and tickets from HedgeDoc.
    sid_cookie = keyring.get_password(KAUF_KEYRING_SERVICENAME, "hedgedoc_sid")

    h = HedgeDocService(hedgedoc_url, sid_cookie=sid_cookie)
    content = h.get_pad_content(hedgedoc_url)

    all_items_ticked = {}

    for line in content.splitlines():
        issue_id = issue_id_from_line(line)
        if not issue_id:
            continue

        if (
            line.startswith("- [x] ") or line.startswith("- [X] ")
        ) and issue_id not in all_items_ticked:
            all_items_ticked[issue_id] = True
        elif line.startswith("- [ ] ") or line.startswith("- [] "):
            all_items_ticked[issue_id] = False

    # Part 2: update the jira issues.
    token = keyring.get_password(KAUF_KEYRING_SERVICENAME, "jira_token")
    if not token:
        msg_error("Missing JIRA token.", command_alt="kauf secrets set jira_token XXX")
    j = JIRAService(token, jira_url)

    finished_issues = [item for item, finished in all_items_ticked.items() if finished]
    if len(finished_issues) == 0:
        msg_success("No issues to update.")
        return

    log_debug(f"will attempt to update issues: {finished_issues}")

    issues = j.search_issues(
        project="EINKAUF",
        keys=finished_issues,
    )

    if len(issues) != len(finished_issues):
        msg_error(
            f"Want to update {len(finished_issues)} issues but can only find {len(issues)}."
        )

    j.execute_transition(issues, transition)

    msg_success(
        f"Updated {len(issues)} issues with the following keys: {[issue.key for issue in issues]}"
    )


def issue_id_from_line(line: str):
    """Parse and return the issue ID in the form 'EINKAUF-XXX'."""
    match = re.search(r"EINKAUF-\d+", line)
    if match:
        return match.group(0)
    return None
