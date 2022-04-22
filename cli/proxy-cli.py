#!/usr/bin/env python3.10
from jinja2 import Template
import typer
import json
import os
import sys
# import logging
# import syslog


haproxy_site_db_location = "db.json"
haproxy_config_template_location = "haproxy_template.jinja"
haproxy_config_location = "haproxy.config"


class ConfigOptions:
    """This class is responsible to generate, reload or test the HAProxy config"""

    def __init__(self):
        self.irony = 1
    
    def reload(self):
        return self

    def generate(self):
        yaml_db = YamlFileManipulations().read()
        template = Template(JinjaReadWrite().read())

        if os.path.exists("/ssl/"):
            if len(os.listdir("/ssl/")) != 0:
                ssl_folder_not_empty = True
        else:
            ssl_folder_not_empty = False
        
        template = template.render(ssl_folder_not_empty=ssl_folder_not_empty, yaml_db=yaml_db)
        return template

    def test(self):
        return self


class YamlFileManipulations:
    """This class is responsible for adding sites, removing sites and editing yaml site DB"""

    def __init__(self, yaml_file: str = haproxy_site_db_location, yaml_input_dict = False):
        self.yaml_file = yaml_file
        self.yaml_input_dict = yaml_input_dict
    

    def read(self):
        if not os.path.exists(self.yaml_file) or os.stat(self.yaml_file).st_size == 0:
            yaml_file = { "sites": [] }
        else:
            with open(self.yaml_file, 'r') as file:
                yaml_file = yaml.safe_load(file)
        return yaml_file

    
    def write(self):
        if self.yaml_input_dict:
            with open(self.yaml_file, 'w') as file:
                yaml.dump(self.yaml_input_dict, file, sort_keys=False)
        else:
            print("There is no input (dictionary) to work with!")
            sys.exit(119)


class SSLCerts:
    """This class is responsible for dealing with SSL certificates"""

    def __init__(self, frontend_adress = False, www_redirection:bool = False, fake:bool = False):
        self.frontend_adress = frontend_adress
        self.www_redirection = www_redirection
        self.fake = fake
    

    def new_cert_from_le(self):
        if not self.frontend_adress:
            message_ = "There was no frontend address set!"
            logging.critical(message_)
            syslog.syslog(syslog.LOG_CRIT, "CRITICAL ERROR! " + message_)
            sys.exit(117)

        command = "certbot certonly --standalone -d " + self.frontend_adress + " --non-interactive --agree-tos --email=slv@yari.pw --http-01-port=8888"
        if self.fake:
            print(command)
        else:
            subprocess.run(command, shell=True, stdout=None)
        # Create SSL check here
        # Copy over new certificates if the operation was successfull
        command = "cat /etc/letsencrypt/live/" + self.frontend_adress + "/fullchain.pem /etc/letsencrypt/live/" + self.frontend_adress + "/privkey.pem > /ssl/" + self.frontend_adress + ".pem"
        if self.fake:
            print(command)
        else:
            subprocess.run(command, shell=True, stdout=None)

        if self.www_redirection:
            command = "certbot certonly --standalone -d www." + self.frontend_adress + " --non-interactive --agree-tos --email=slv@yari.pw --http-01-port=8888"
            if self.fake:
                print(command)
            else:
                subprocess.run(command, shell=True, stdout=None)

            # Create SSL check here
            # Copy over new certificates if the operation was successfull

            command = "cat /etc/letsencrypt/live/www." + self.frontend_adress + "/fullchain.pem /etc/letsencrypt/live/www." + self.frontend_adress + "/privkey.pem > /ssl/www." + self.frontend_adress + ".pem"
            if self.fake:
                print(command)
            else:
                subprocess.run(command, shell=True, stdout=None)

        status = ("Success", "Failure")
        return status


    def init(self):
        yaml_db = YamlFileManipulations().read()
        for site in yaml_db["sites"]:
            www_redirection = site.get("www_redirection", False)
            frontend_adress = site["site_name"]
            SSLCerts(frontend_adress=frontend_adress, www_redirection=www_redirection, fake=self.fake).new_cert_from_le()


    def create_self_signed(self):
        return self
    
    def retire_cert(self):
        # Copy the old cert to "archive" folder before renewal
        return self
    
    def renew_cert(self):
        # Call test_cert function to determine if renewal is needed
        # Call retire function
        # Call new_cert function
        # Return status
        return self

    def test_cert(self):
        # Check if cert exists
        # Check the date on cert
        # Return status
        return self
    
    def check_if_exist(self):
        return self


class JinjaReadWrite:
    """This class is responsible for Jinja2 template file handling"""

    def __init__(self, haproxy_config_template = haproxy_config_template_location):
        self.haproxy_config_template = haproxy_config_template
        if not os.path.exists(self.haproxy_config_template):
            message_ = "Template file doesn't exist!"
            logging.critical(message_)
            syslog.syslog(syslog.LOG_CRIT, "CRITICAL ERROR! " + message_)
            sys.exit(118)

    def read(self):
        with open(self.haproxy_config_template, 'r') as file:
            haproxy_config_template = file.read()
        return haproxy_config_template


""" Code below is responsible for CLI """

app = typer.Typer(context_settings=dict(max_content_width=800))


@app.command()
def config(reload:bool=typer.Option(False, help="Generate, test and reload the config"), \
    generate:bool=typer.Option(False, help="Only generate new config (used for troubleshooting)"), \
    test:bool=typer.Option(False, help="Generate and test the new config (used for troubleshooting)"), \
    show:bool=typer.Option(False, help="Print out the latest config"), \
        ):
    
    '''
    This argument directly deals with HAProxy config. Example proxy_manager.py --show
    '''

    if (reload and generate) or (reload and test) or (generate and test):
        print("You can't use these options together!")
        sys.exit(120)
    elif not (reload or generate or test or show):
        logging.error("You have to choose at least 1 parameter! Use --help option to find the approptiate flags.")
        sys.exit(116)

    if show:
        print(ConfigOptions().generate())


@app.command()
def site_db():

    """
    site-db shows site database in the form of YAML console output
    """
    
    yaml_db = yaml.dump(YamlFileManipulations().read(), sort_keys=False)
    print(yaml_db)
    

@app.command()
def site_db_add(site_name:str=typer.Argument(..., help="Add new site to the database."),
    owner:str=typer.Option("", help="Specify site owner"),
    cert_type:str=typer.Option("certbot", help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
    active:bool=typer.Option(True, help="Use HTTP/2 on the backend"),
    www_redirection:bool=typer.Option(False, help="Activate \"www -> root domain\" redirection"),
    backend_servers:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
    backend_http2:bool=typer.Option(False, help="Use HTTP/2 on the backend"),
    backend_https:bool=typer.Option(False, help="Use HTTPs on the backend"),
    x_realip:bool=typer.Option(False, help="Use X-Real-IP instead of Forwarded-IP"),
    ):

    """
    This argument deals with adding new sites to our YAML database.
    Example: proxy_manager.py site-db-add gateway-it.com --backend-servers 192.168.1.1:443,192.168.2.1:443 --backend-http2 --backend-https
    """

    site = {}
    site["site_name"] = site_name
    site["active"] = active
    site["cert_type"] = cert_type
    site["www_redirection"] = www_redirection
    site["use_x_realip"] = x_realip
    if owner:
        site["owner"] = owner
    
    site["backend_servers"] = []
    for backend_server in backend_servers.split(","):
        backend_server_dict = {}
        backend_server_dict["backend_server_address"] = backend_server
        backend_server_dict["backend_server_http2"] = backend_http2
        backend_server_dict["backend_server_https"] = backend_https
        site["backend_servers"].append(backend_server_dict)

    yaml_db = YamlFileManipulations().read()

    for site_name in yaml_db["sites"]:
        if site_name["site_name"] == site["site_name"]:
            print("The site " + site["site_name"] + " already exists in our database!")
            sys.exit(1)
    
    yaml_db["sites"].append(site)

    YamlFileManipulations(yaml_input_dict=yaml_db).write()


@app.command()
def site_db_update(site_name:str=typer.Argument(..., help="Add new site to the database."),
    owner:str=typer.Option(..., help="Specify site owner"),
    cert_type:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
    active:bool=typer.Option(..., help="Use HTTP/2 on the backend"),
    www_redirection:bool=typer.Option(..., help="Activate \"www -> root domain\" redirection"),
    backend_servers:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
    backend_http2:bool=typer.Option(..., help="Use HTTP/2 on the backend"),
    backend_https:bool=typer.Option(..., help="Use HTTPs on the backend"),
    x_realip:bool=typer.Option(..., help="Use X-Real-IP instead of Forwarded-IP"),
    ):

    """
    This argument deals with updating sites in our YAML database.
    Example: proxy_manager.py site-db-update gateway-it.com --backend-servers 192.168.1.1:443,192.168.2.1:443 --backend-http2 --backend-https
    """    

    yaml_db = YamlFileManipulations().read()

    for site_name in yaml_db["sites"]:
        if site_name["site_name"] == site["site_name"]:
            print("The site " + site["site_name"] + " already exists in our database!")
            sys.exit(1)


@app.command()
def site_db_remove(site_name:str=typer.Argument(..., help="Site address")):
    """
    This argument deals with removing sites from YAML database.
    Example: proxy_manager.py site-db-remove gateway-it.com
    """
    
    yaml_db = YamlFileManipulations().read()
    yaml_db_lenght = len(yaml_db["sites"])
    
    if yaml_db_lenght == 0:
        print("The database list is empty! Please add one or more websites.")
        sys.exit(1)

    for site_number in range(0, yaml_db_lenght):
        site_name_inThisLoop = yaml_db["sites"][site_number]["site_name"]
        if site_name == site_name_inThisLoop:
            del yaml_db["sites"][site_number]
            print("The site " + site_name + " was removed from our database!")
            YamlFileManipulations(yaml_input_dict=yaml_db).write()
            sys.exit(0)
        elif site_name != site_name_inThisLoop and site_number == yaml_db_lenght-1:
            print("Site was not found in our database!")
            break
    

@app.command()
def site_db_be_add(site_name:str=typer.Argument(..., help="Add new site to the database."),
    be:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
    ):

    """
    This argument deals with add site backends to our YAML database.
    Example: proxy_manager.py site-db-update gateway-it.com --backend-servers 192.168.1.1:443,192.168.2.1:443 --backend-http2 --backend-https
    """    

    yaml_db = YamlFileManipulations().read()

    for site_name in yaml_db["sites"]:
        if site_name["site_name"] == site["site_name"]:
            print("The site " + site["site_name"] + " already exists in our database!")
            sys.exit(1)


@app.command()
def site_db_be_remove(site_name:str=typer.Argument(..., help="Add new site to the database."),
    be:str=typer.Option(..., help="Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443"),
    ):

    """
    This argument deals with removing site backends from our YAML database.
    Example: proxy_manager.py site-db-update gateway-it.com --backend-servers 192.168.1.1:443,192.168.2.1:443 --backend-http2 --backend-https
    """    

    yaml_db = YamlFileManipulations().read()

    for site_name in yaml_db["sites"]:
        if site_name["site_name"] == site["site_name"]:
            print("The site " + site["site_name"] + " already exists in our database!")
            sys.exit(1)


@app.command()
def certificate(
    request:str=typer.Option("", help="Request a new certificate from LetsEncrypt and copy it over to /ssl/ folder"),
    self_signed:str=typer.Option("", help="Generate a new self signed certificate and copy it over to /ssl/ folder"),
    init:bool=typer.Option(False, help="Generate a new self signed certificate and copy it over to /ssl/ folder"),
    renew:str=typer.Option("", help="Renews the certificate for a given site name"),
    test:str=typer.Option("", help="Test a given certificate for validity"),
    fake:bool=typer.Option(False, help="Print executable commands to the screen (useful for debugging)"),
    www_redirection:bool=typer.Option(False, help="Print executable commands to the screen (useful for debugging)"),
    ):

    """
    This argument deals with SSL certificates.
    Example: proxy_manager.py certificate --init
    """
    
    if not (request or self_signed or renew or test or init):
        logging.error("You have to choose at least 1 parameter! Use --help option to find the approptiate flags.")
        sys.exit(116)
    
    if init:
        SSLCerts(fake=fake).init()
    elif request:
        SSLCerts(fake=fake, frontend_adress=request, www_redirection=www_redirection).new_cert_from_le()


if __name__ == "__main__":
    app()