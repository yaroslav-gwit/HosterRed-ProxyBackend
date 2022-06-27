# SYSTEM IMPORTS
import sys

# 3RD PARTY IMPORTS
import typer
import yaml

# INTERNAL IMPORTS
from cli import internal_classes as IC


app = typer.Typer(context_settings=dict(max_content_width=800))

@app.command()
def show():
    """
    site-db shows site database in the form of YAML console output
    """
    yaml_db = yaml.dump(IC.YamlFileManipulations().read(), sort_keys=False)
    print(yaml_db)


@app.command()
def add(site_name:str=typer.Argument(..., help="Frontend address"),
        owner:str=typer.Option("System", help="Specify site owner"),
        cert_type:str=typer.Option("automatic", help="Certificate type: automatic/manual/selfsigned"),
        active:bool=typer.Option(True, help="Use HTTP/2 on the backend"),
        www_redirection:bool=typer.Option(False, help="Activate \"www -> root domain\" redirection"),
        backends:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
        be_http2:bool=typer.Option(True, help="Use HTTP/2 on the backend"),
        be_https:bool=typer.Option(True, help="Use HTTPs on the backend"),
        be_health_check:bool=typer.Option(False, help="Check if backend server is alive"),
        x_realip:bool=typer.Option(False, help="Use X-Real-IP instead of Forwarded-IP"),
    ):

    """
    This argument deals with adding new sites to our YAML database.
    """

    site = {}
    site["site_name"] = site_name
    site["active"] = active
    site["cert_type"] = cert_type
    site["www_redirection"] = www_redirection
    site["use_x_realip"] = x_realip
    site["owner"] = owner
    
    site["backend_servers"] = []
    for backend_server in backends.split(","):
        backend_server_dict = {}
        backend_server_dict["backend_server_address"] = backend_server
        backend_server_dict["backend_server_http2"] = be_http2
        backend_server_dict["backend_server_https"] = be_https
        backend_server_dict["backend_server_health_check"] = be_health_check
        site["backend_servers"].append(backend_server_dict)

    yaml_db = IC.YamlFileManipulations().read()

    for site_name in yaml_db["sites"]:
        if site_name["site_name"] == site["site_name"]:
            print("The site " + site["site_name"] + " already exists in our database!", file=sys.stderr)
            sys.exit(1)
    
    yaml_db["sites"].append(site)

    IC.YamlFileManipulations(yaml_input_dict=yaml_db).write()


@app.command()
def remove(site_name:str=typer.Argument(..., help="Site address")):
    """
    This argument deals with removing sites from YAML database.
    """
    
    yaml_db = IC.YamlFileManipulations().read()
    yaml_db_lenght = len(yaml_db["sites"])
    
    if yaml_db_lenght == 0:
        print("The database list is empty! Please add one or more websites.")
        sys.exit(1)

    for site_number in range(0, yaml_db_lenght):
        site_name_inThisLoop = yaml_db["sites"][site_number]["site_name"]
        if site_name == site_name_inThisLoop:
            del yaml_db["sites"][site_number]
            print("The site " + site_name + " was removed from our database!")
            IC.YamlFileManipulations(yaml_input_dict=yaml_db).write()
            sys.exit(0)
        elif site_name != site_name_inThisLoop and site_number == yaml_db_lenght-1:
            print("Site was not found in our database!")
            break


# @app.command()
# def update(site_name:str=typer.Argument(..., help="Add new site to the database."),
#         owner:str=typer.Option(..., help="Specify site owner"),
#         cert_type:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
#         active:bool=typer.Option(..., help="Use HTTP/2 on the backend"),
#         www_redirection:bool=typer.Option(..., help="Activate \"www -> root domain\" redirection"),
#         backend_servers:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
#         backend_http2:bool=typer.Option(..., help="Use HTTP/2 on the backend"),
#         backend_https:bool=typer.Option(..., help="Use HTTPs on the backend"),
#         x_realip:bool=typer.Option(..., help="Use X-Real-IP instead of Forwarded-IP"),
#     ):
#     """
#     This argument deals with updating sites in our YAML database.
#     Example: proxy_manager.py site-db-update gateway-it.com --backend-servers 192.168.1.1:443,192.168.2.1:443 --backend-http2 --backend-https
#     """    

#     yaml_db = IC.YamlFileManipulations().read()

#     for site_name in yaml_db["sites"]:
#         if site_name["site_name"] == site_name:
#             print("The site " + site_name + " already exists in our database!")
#             sys.exit(1)





# @app.command()
# def backend_add(site_name:str=typer.Argument(..., help="Add new site to the database."),
#         backend:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
#     ):

#     """
#     This argument deals with add site backends to our YAML database.
#     Example: proxy_manager.py site-db-update gateway-it.com --backend-servers 192.168.1.1:443,192.168.2.1:443 --backend-http2 --backend-https
#     """    

#     yaml_db = IC.YamlFileManipulations().read()

#     for site_name in yaml_db["sites"]:
#         if site_name["site_name"] == site_name:
#             print("The site " + site_name + " already exists in our database!")
#             sys.exit(1)


# @app.command()
# def backend_remove(site_name:str=typer.Argument(..., help="Add new site to the database."),
#     be:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
#     ):

#     """
#     This argument deals with removing site backends from our YAML database.
#     Example: proxy_manager.py site-db-update gateway-it.com --backend-servers 192.168.1.1:443,192.168.2.1:443 --backend-http2 --backend-https
#     """    

#     yaml_db = IC.YamlFileManipulations().read()

#     for site_name in yaml_db["sites"]:
#         if site_name["site_name"] == site_name:
#             print("The site " + site_name + " already exists in our database!")
#             sys.exit(1)


""" If this file is executed from the command line, activate Typer """
if __name__ == "__main__":
    app()