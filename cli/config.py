#!/usr/bin/env python3

# 3rd party imports
from distutils.command.config import config
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

@app.command()
def generate(
    ):
    """
    Generate new config and reload the HAProxy service
    """
    config_file_location = "/etc/haproxy/haproxy.cfg"
    config_file_content = IC.ConfigOptions().generate()

    with open(config_file_location, "w") as file:
        file.write(config_file_content)
    print("New config file was written to: " + config_file_location)
    
    IC.ConfigOptions().reload()
    print("Service was reloaded")


""" If this file is executed from the command line, activate Typer """
if __name__ == "__main__":
    app()