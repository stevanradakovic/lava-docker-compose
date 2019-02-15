#!/bin/bash

set -ex
squad-admin migrate
# this part should be changed when proper commands are available in squad
squad-admin createsuperuser --noinput --username ${SQUAD_ADMIN_USER} --email admin@example.com || true
ADMIN_TOKEN_STRING=$(squad-admin drf_create_token ${SQUAD_ADMIN_USER})
ADMIN_TOKEN=$(echo ${ADMIN_TOKEN_STRING} | cut -d ' ' -f 3)

# create usergroup, group, project and CI backend using API
python3 create_objects.py --url http://squad-web:8000/api/ --token "${ADMIN_TOKEN}" --lava-url http://lava.server/RPC2/ --lava-username ${LAVA_SQUAD_USER} --lava-token ${LAVA_SQUAD_TOKEN}
