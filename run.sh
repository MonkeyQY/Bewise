#!/bin/bash

#
# This file should be used to prepare and run your WebProxy after setting up your .env file
# Source: https://github.com/evertramos/docker-compose-letsencrypt-nginx-proxy-companion
#

# 1. Check if .env file exists
if [ -e .env ]; then
    source .env
else
    echo "Please set up your .env file before starting your environment."
    exit 1
fi

# 2. Download the latest version of nginx.tmpl
curl https://raw.githubusercontent.com/jwilder/nginx-proxy/master/nginx.tmpl > nginx.tmpl


# 3. Install Loki Docker driver plugin
docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

# 4. Start proxy
docker compose up -d


exit 0