#!/usr/bin/env bash
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root!"
    exit 1
fi

if [[ ! -d /opt/hoster_red_proxy ]]; then
    mkdir /opt/hoster_red_proxy
    git clone https://github.com/yaroslav-gwit/HosterRed-ProxyBackend.git /opt/hoster_red_proxy/
    cat /opt/hoster_red_proxy/proxy-cli.sh > /bin/proxy-cli
    chmod +x /bin/proxy-cli
    cd /opt/hoster_red_proxy/
    apt install python3-pip python3-venv
    python3 -m venv .
    source bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    echo "Proxy Manager has been installed!"
else
    cd /opt/hoster_red_proxy/
    git pull
    source bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    cat /opt/hoster_red_proxy/proxy-cli.sh > /bin/proxy-cli
    chmod +x /bin/proxy-cli
    echo "Proxy Manager has been upgraded!"
fi
