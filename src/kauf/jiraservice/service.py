from jira import JIRA

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

    def search_issues(self, project: str = None, labels: list[str] = None):
        conditions = []
        if project:
            conditions.append("project = " + project)
        if labels:
            conditions.append("labels in (" + ", ".join(labels) + ")")

        return self.jira.search_issues(" and ".join(conditions))
