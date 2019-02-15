#!/bin/bash

set -ex
squad-admin migrate
# this part should be changed when proper commands are available in squad
squad-admin createsuperuser --noinput --username ${SQUAD_ADMIN_USER} --email admin@example.com || true
ADMIN_TOKEN_STRING=$(squad-admin drf_create_token ${SQUAD_ADMIN_USER})
ADMIN_TOKEN=$(echo ${ADMIN_TOKEN_STRING} | cut -d ' ' -f 3)

# create usergroup, group, project and CI backend using API
# django URLField doesn't accept 'lava_server' as address. Convert to IP address.
LAVA_SERVER_IP=$(getent hosts lava_server | awk '{ print $1 }')
python3 create_objects.py --url http://squad-web:8000/api/ --token "${ADMIN_TOKEN}" --lava-url http://${LAVA_SERVER_IP}/RPC2/ --lava-username ${LAVA_ADMIN_USER} --lava-token ${LAVA_SQUAD_TOKEN}
