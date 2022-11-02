#!/usr/bin/env bash
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root!"
    exit 1
fi

apt install -y certbot haproxy

if [[ ! -d /ssl/ ]]; then
    mkdir /ssl/
fi

chmod g-w /ssl/
chmod o-w /ssl/
chmod g+r /ssl/
chmod o+r /ssl/
chmod g+x /ssl/
chmod o+x /ssl/
for FILE in $(ls -1 /ssl/); do
    chmod g-w /ssl/$FILE
    chmod g-x /ssl/$FILE
    chmod o-w /ssl/$FILE
    chmod o-x /ssl/$FILE
    chmod g+r /ssl/$FILE
    chmod o+r /ssl/$FILE
done


if [[ ! -d /opt/hoster_red_proxy ]]; then
    mkdir /opt/hoster_red_proxy
    git clone https://github.com/yaroslav-gwit/HosterRed-ProxyBackend.git /opt/hoster_red_proxy/
    cat /opt/hoster_red_proxy/proxy-cli.sh > /bin/proxy-cli
    chmod +x /bin/proxy-cli
    cd /opt/hoster_red_proxy/
    git config pull.rebase false
    apt install python3-pip python3-venv haproxy
    python3 -m venv .
    source bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    echo
    echo
    echo
    echo "Proxy Manager has been installed!"
else
    cd /opt/hoster_red_proxy/
    git config pull.rebase false
    git pull
    source bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    cat /opt/hoster_red_proxy/proxy-cli.sh > /bin/proxy-cli
    chmod +x /bin/proxy-cli
    echo
    echo
    echo
    echo "Proxy Manager has been upgraded!"
fi
