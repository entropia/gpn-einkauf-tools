from jira import JIRA, Issue

from kauf.format import msg_error
from kauf.format.log import log_debug


class JIRAService:
    token: str
    jira: JIRA

    def __init__(self, token: str, server: str):
        self.token = token

        if not server.startswith("http://") or server.startswith("https://"):
            server = "https://" + server

        self.jira = JIRA(token_auth=token, server=server)

    def get_projects(self):
        projects = self.jira.projects()
        log_debug(f"got projects: {[p.name for p in projects]}")
        return projects

    def search_issues(
        self,
        project: str = None,
        labels: list[str] = None,
        status_exclude: list[str] = None,
        keys: list[str] = None,
    ):
        """
        Search for JIRA issues.

        :param project: Optional name of the project to filter for.
        :type project: str
        :param labels: Optional list of labels to filter for.
        :type labels: list[str]
        :param status_exclude: Optional list of issue statuses to exclude.
        :type status_exclude: list[str]
        :param keys: Optional list of issue keys to filter for.
        :type keys: list[str]
        """
        conditions = []
        if project:
            conditions.append("project = " + project)
        if labels:
            conditions.append("labels in (" + ", ".join(labels) + ")")
        if status_exclude:
            conditions.append("status not in (" + ", ".join(status_exclude) + ")")
        if keys:
            conditions.append("key in (" + ", ".join(keys) + ")")

        return self.jira.search_issues(" and ".join(conditions))

    def execute_transition(
        self,
        issues: list[Issue],
        transition: str,
    ):
        # Hacky, expects all issues to be from the same project to avoid collisions in transition naming.
        transition_name_to_id = {}

        # Check first if all issues support the desired transition before applying it.
        for issue in issues:
            available_transitions = []
            for t in self.jira.transitions(issue):
                available_transitions.append(t["name"])
                transition_name_to_id[t["name"]] = t["id"]

            if transition not in available_transitions:
                msg_error(
                    f"Issue '{issue.key}' does not support transition '{transition}'. Available transitions are: {available_transitions}"
                )

        for issue in issues:
            self.jira.transition_issue(issue, transition_name_to_id[transition])
