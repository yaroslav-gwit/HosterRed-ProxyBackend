#!/usr/bin/env python3

# 3rd party imports
import typer

# internal imports
from cli import internal_classes as IC


""" Section below is responsible for the CLI input/output """
app = typer.Typer(context_settings=dict(max_content_width=800))


@app.command()
def reload(
    fake:bool=typer.Option(False, help="Print out the commands (no execution!)"),
    ):
    """
    Reload the config
    """
    IC.ConfigOptions(fake=fake).reload()


@app.command()
def show(
    ):
    """
    Print out the config
    """
    print(IC.ConfigOptions().generate())


""" If this file is executed from the command line, activate Typer """
if __name__ == "__main__":
    app()