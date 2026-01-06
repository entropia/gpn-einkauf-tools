import typer

from .callback import callback

from .jiraservice.cmd_health import jira_app
from .secrets import secrets_app

app = typer.Typer(callback=callback)
app.add_typer(jira_app, name="jira")
app.add_typer(secrets_app, name="secrets")

if __name__ == "__main__":
    app()
