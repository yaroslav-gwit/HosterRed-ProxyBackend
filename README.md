# HosterRed-ProxyBackend
## Project overview
This is a set of Python CLI scripts to generate a reverse proxy (HTTPs only for now) configs for HAProxy. Simplicity is a key in my projects, so as a result a single YAML file is used as a database to keep all of the sites you need. Please keep in mind that at the moment only Debian 11 is officially supported as a host OS.
### Installation
To get started with this project run an installation script (as root!):
```
curl https://raw.githubusercontent.com/yaroslav-gwit/HosterRed-ProxyBackend/main/install.sh | bash
```

Or with debugging enabled:
```
curl https://raw.githubusercontent.com/yaroslav-gwit/HosterRed-ProxyBackend/main/install.sh | bash -x
```

### Updates
To get the latest updates, just run the installation script again. It will update everything automatically if the software is already installed.
```
curl https://raw.githubusercontent.com/yaroslav-gwit/HosterRed-ProxyBackend/main/install.sh | bash
```

## Using the script
There is a built-in documentation for (almost) every feature in this small library. Just use a `--help` flag to get it:
```
proxy-cli --help
```
Add a new site to the database:
```
proxy-cli add gateway-it.com --backends 192.168.120.10:443,192.168.120.11:443 --www-redirection --be-http2 --be-https --be-health-check --x-realip
```
Execute this command to check the flags you need to include/exclude from the command above:
```
proxy-cli database add --help

# Example output:
Usage: proxy-cli database add [OPTIONS] SITE_NAME

  This argument deals with adding new sites to our YAML database.

Arguments:
  SITE_NAME  Frontend address  [required]

Options:
  --owner TEXT                    Specify site owner  [default: System]
  --cert-type TEXT                Certificate type: automatic/manual/selfsigned  [default: automatic]
  --active / --no-active          Use HTTP/2 on the backend  [default: active]
  --www-redirection / --no-www-redirection
                                  Activate "www -> root domain" redirection  [default: no-www-redirection]
  --backends TEXT                 Backend servers, coma separated: 1.1.1.1:433,2.2.2.2:8443  [required]
  --be-http2 / --no-be-http2      Use HTTP/2 on the backend  [default: be-http2]
  --be-https / --no-be-https      Use HTTPs on the backend  [default: be-https]
  --be-health-check / --no-be-health-check
                                  Check if backend server is alive  [default: no-be-health-check]
  --x-realip / --no-x-realip      Use X-Real-IP instead of Forwarded-IP  [default: no-x-realip]
  --help                          Show this message and exit.
```

Finally execute the command below to get all of the certificates for active websites:
```
proxy-cli certificate init
```
