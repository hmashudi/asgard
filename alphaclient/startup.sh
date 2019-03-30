#!/bin/sh
/usr/sbin/sshd -D -E /var/log/sshd.log &

python3 ./alphaclient.py
