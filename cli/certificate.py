#!/usr/bin/env python3
import datetime

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

@app.command()
def check(
        address:str=typer.Argument(..., help="Site address"),
    ):
    """
    Check if valid certificate exists for a given site
    """
    
    response = IC.SSLCerts.test_cert(site_address=address)
    cert_status = response["cert_status"]
    cert_end_date = response["cert_end_date"]
    cert_end_date = str(cert_end_date.year) + "/" + str(cert_end_date.month) + "/" + str(cert_end_date.day)
    print("Certificate status: " + cert_status)
    print("Certificate end date: " + cert_end_date)


""" If this file is executed from the command line, activate Typer """
if __name__ == "__main__":
    app()
