#!/bin/bash
iptables -F
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
cd compose-postgres && docker-compose restart
