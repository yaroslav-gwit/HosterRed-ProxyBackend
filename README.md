# HosterRed-ProxyBackend
## Project overview
This is a set of Python CLI scripts to generate a reverse proxy (HTTPs only for now) configs for HAProxy. Simplicity is a key in my projects, so as a result a single YAML file is used as a database to keep all of the sites you need. Please keep in mind that at the moment only Debian 11 is supported as a host OS.
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
These is a built-in documentation for (almost) every feature in this small library. Just use a `--help` flag to get it:
```
proxy-cli --help
```
