#!/bin/bash

HOST=$(jq -r '.host' config.json)
PORT=$(jq -r '.port' config.json)
USERNAME=$(jq -r '.username' config.json)
PASSWORD=$(jq -r '.password' config.json)

getRouterIp() {
  sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -p "$PORT" "$USERNAME@$HOST" \
  "ifconfig ppp0 | head -n 2 | tail -n 1" | awk '{print $2}' | sed 's/addr://'
}

getPublicIp() {
  curl -s https://api.ipify.org
}

ROUTER_IP=$(getRouterIp)
PUBLIC_IP=$(getPublicIp)

if [[ "$ROUTER_IP" != "$PUBLIC_IP" ]]; then
  echo "bad $ROUTER_IP $PUBLIC_IP"
fi

if [[ "$ROUTER_IP" == "$PUBLIC_IP" ]]; then
  echo "good $ROUTER_IP $PUBLIC_IP"
fi
