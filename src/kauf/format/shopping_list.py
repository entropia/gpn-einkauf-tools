from jira import Issue
import re


class ShoppingList:
    class Item:
        name: str
        shop: str
        issue_key: str
        item_url: str | None = None

        def __init__(
            self, name: str, shop: str, issue_key: str, url: str | None = None
        ):
            self.name = name
            self.item_url = url
            self.issue_key = issue_key
            self.shop = shop

    def __init__(self, issues: Issue, base_url: str):
        self.issues = issues

        if not base_url.startswith("http://") or base_url.startswith("https://"):
            base_url = "https://" + base_url
        self.base_url = base_url
        self._get_items()

    items: list[Item] = []

    def _get_items(self):
        for issue in self.issues:
            issue_items = issue.description.splitlines()

            for item in issue_items:
                if len(item) <= 2:
                    continue

                item = item.strip().removeprefix("- ").removeprefix("* ")

                # Try to find URL in item.
                url = None
                url_group = re.search("(?P<url>https?://[^\s]+)", item)
                if url_group:
                    url = url_group.group("url")
                    item = item.replace(url, "")

                self.items.append(
                    ShoppingList.Item(
                        item, str(issue.fields.customfield_11907), issue.key, url=url
                    )
                )

    def as_markdown(self):
        itemsPerShop = {}

        for item in self.items:
            if item.shop in itemsPerShop:
                itemsPerShop[item.shop].append(item)
            else:
                itemsPerShop[item.shop] = [item]

        lines = []
        for shop, items in itemsPerShop.items():
            lines.append("### " + shop)
            for item in items:
                line = f"- [ ] {item.name} ([{item.issue_key}]({self.base_url}/browse/{item.issue_key})"

                if item.item_url:
                    line += f"; [Produkt]({item.item_url})"

                line += ")"

                lines.append(line)

        return "\n".join(lines)
