from jira import Issue
import re


class ShoppingList:
    class Item:
        name: str
        issue_key: str
        url: str | None = None

        def __init__(self, name: str, issue_key: str, url: str | None = None):
            self.name = name
            self.url = url
            self.issue_key = issue_key

    def __init__(self, issues: Issue):
        self.issues = issues
        self._get_items()

    items: list[Item] = []

    def _get_items(self):
        for issue in self.issues:
            issue_items = issue.fields.customfield_11004.splitlines()

            for item in issue_items:
                if len(item) <= 2:
                    continue

                item = item.removeprefix("- ").removeprefix("* ")

                # Try to find URL in item.
                url = None
                url_group = re.search("(?P<url>https?://[^\s]+)", item)
                if url_group:
                    url = url_group.group("url")
                    item = item.replace(url, "")

                self.items.append(ShoppingList.Item(item, issue.key, url=url))

    def as_markdown(self):
        lines = []
        for item in self.items:
            line = f"- {item.name} ({item.issue_key}"

            if item.url:
                line += f"; [Produkt]({item.url})"

            line += ")"

            lines.append(line)

        return "\n".join(lines)
