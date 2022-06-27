#!/usr/bin/env python3
# NATIVE IMPORTS
import datetime
import os
import sys
import subprocess

# 3RD PARTY MODULES
from cryptography.x509 import load_pem_x509_certificate as load_pem_cert
import yaml
from jinja2 import Template


# FILE LOCATIONS
haproxy_site_db_location = "db.yml"
haproxy_config_template_location = "haproxy_template.jinja"
haproxy_config_location = "/etc/haproxy/haproxy.cfg"


# class FileLocations:
#     def __init__(self):
#         self.haproxy_site_db_location = "db.yml"
#         self.haproxy_config_template_location = "haproxy_template.jinja"
#         self.haproxy_config_location = "/etc/haproxy/haproxy.cfg"


class YamlFileManipulations:
    """This class is responsible for adding sites, removing sites and editing yaml site DB"""

    def __init__(self, yaml_file:str = haproxy_site_db_location, yaml_input_dict = False):
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
            sys.exit(117)

        command = "certbot certonly --standalone -d " + self.frontend_adress + " --non-interactive --agree-tos --email=slv@yari.pw --http-01-port=8888"
        if self.fake:
            print(command)
        else:
            subprocess.run(command, shell=True)
        # Create SSL check here
        # Copy over new certificates if the operation was successfull
        command = "cat /etc/letsencrypt/live/" + self.frontend_adress + "/fullchain.pem /etc/letsencrypt/live/" + self.frontend_adress + "/privkey.pem > /ssl/" + self.frontend_adress + ".pem"
        if self.fake:
            print(command)
        else:
            subprocess.run(command, shell=True)

        if self.www_redirection:
            command = "certbot certonly --standalone -d www." + self.frontend_adress + " --non-interactive --agree-tos --email=slv@yari.pw --http-01-port=8888"
            if self.fake:
                print(command)
            else:
                subprocess.run(command, shell=True)

            # Create SSL check here
            # Copy over new certificates if the operation was successfull

            command = "cat /etc/letsencrypt/live/www." + self.frontend_adress + "/fullchain.pem /etc/letsencrypt/live/www." + self.frontend_adress + "/privkey.pem > /ssl/www." + self.frontend_adress + ".pem"
            if self.fake:
                print(command)
            else:
                subprocess.run(command, shell=True)

        status = ("Success", "Failure")
        return status


    def init(self):
        yaml_db = YamlFileManipulations().read()
        for site in yaml_db["sites"]:
            www_redirection = site.get("www_redirection", False)
            frontend_adress = site["site_name"]
            cert_validity = SSLCerts.test_cert(frontend_adress)
            if cert_validity["cert_status"] != "valid":
                SSLCerts(frontend_adress=frontend_adress, www_redirection=www_redirection, fake=self.fake).new_cert_from_le()
            else:
                print("Certificate is up-to-date: " + frontend_adress)

        ConfigOptions().reload()


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

    @staticmethod
    def test_cert(site_address:str):
        cert_file = "/ssl/" + site_address + ".pem"
        delta = datetime.datetime.today() + datetime.timedelta(weeks=2)
        if os.path.exists(cert_file):
            with open(cert_file, "r") as file:
                cert = file.read().encode('ascii')
            try:
                cert = load_pem_cert(cert)
                cert_site_name = str(cert.subject).replace("<Name(CN=", "").replace(")>", "")
                cert_end_date = cert.not_valid_after
                
                if site_address == cert_site_name and cert_end_date > delta:
                    cert_status = "valid"
                else:
                    cert_status = "invalid"
            except:
                cert_status = "Not a certificate!"
                cert_end_date = "N/A"

        return {"cert_status": cert_status, "cert_end_date": cert_end_date}


class ConfigOptions:
    """This class is responsible to generate, reload or test the HAProxy config"""

    def __init__(self, fake=False):
        self.fake = fake

    def reload(self):
        command = "systemctl reload haproxy"
        if self.fake:
            print(command)
        else:
            subprocess.run(command, shell=True)

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


class JinjaReadWrite:
    """This class is responsible for Jinja2 template file handling"""

    def __init__(self, haproxy_config_template = haproxy_config_template_location):
        self.haproxy_config_template = haproxy_config_template
        if not os.path.exists(self.haproxy_config_template):
            message_ = "Template file doesn't exist!"
            sys.exit(118)

    def read(self):
        with open(self.haproxy_config_template, 'r') as file:
            haproxy_config_template = file.read()
        return haproxy_config_template