#!/usr/bin/env bash
if [[ ! -z $1 ]]; then
    cd /opt/hoster_red_proxy/
    source bin/activate
    python3 proxy-cli $@
else
    cd /opt/hoster_red_proxy/
    source bin/activate
    python3 proxy-cli --help