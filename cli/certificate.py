#!/usr/bin/env python3

# 3rd party imports
import typer

# internal imports
from cli import internal_classes as IC


""" Section below is responsible for the CLI input/output """
app = typer.Typer(context_settings=dict(max_content_width=800))


@app.command()
def request(
        address:str=typer.Argument(..., help="Site address"),
        include_www:bool=typer.Option(False, help="Turn on WWW redirection"),
        fake:bool=typer.Option(False, help="Print out the commands (no execution!)"),
    ):
    """
    Request a new SSL certificate
    """
    
    IC.SSLCerts(fake=fake, frontend_adress=address, www_redirection=include_www).new_cert_from_le()


@app.command()
def init(
        fake:bool=typer.Option(False, help="Print out the commands (no execution!)"),
    ):
    """
    Generate all missing certificates
    """
    
    IC.SSLCerts(fake=fake).init()


""" If this file is executed from the command line, activate Typer """
if __name__ == "__main__":
    app()
