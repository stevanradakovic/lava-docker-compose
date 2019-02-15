import argparse
import json
import requests
import sys
from copy import deepcopy
try:
    from urllib.parse import urlparse, urljoin
except:
    from urlparse import urlparse, urljoin

USERGROUPS_ENDPOINT = "/api/usergroups/"
GROUPS_ENDPOINT = "/api/groups/"
PROJECTS_ENDPOINT = "/api/projects/"
BACKENDS_ENDPOINT = "/api/backends/"


def find_or_create(url, object_dict, headers):
    modified_object_dict = deepcopy(object_dict)
    if "group" in object_dict.keys():
        group = modified_object_dict["group"].split("/")[-2]
        modified_object_dict["group"] = group
    obj_response = requests.get(url, params=modified_object_dict, headers=headers)
    obj = None
    if obj_response.status_code == 200:
        if obj_response.json()['count'] == 1:
            return obj_response.json()['results'][0]['url']
        else:
            obj_response2 = requests.post(url, json=object_dict, headers=headers)
            if obj_response2.status_code == 201:
                return obj_response2.json()['url']
            else:
                print(obj_response2.text)
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        "--token",
                        help="Token used for authorization",
                        required=True,
                        dest="token")
    parser.add_argument("-v",
                        "--debug",
                        action="store_true",
                        default=False,
                        help="Enable debug",
                        dest="debug")
    parser.add_argument("-u",
                        "--url",
                        help="SQUAD instance URL",
                        required=True,
                        dest="url")
    parser.add_argument("-l",
                        "--lava-url",
                        help="LAVA URL",
                        required=True,
                        dest="lava_url")
    parser.add_argument("-w",
                        "--lava-username",
                        help="LAVA username",
                        required=True,
                        dest="lava_user")
    parser.add_argument("-p",
                        "--lava-token",
                        help="LAVA authentication token",
                        required=True,
                        dest="lava_token")

    args = parser.parse_args()

    headers = {
        "Authorization": "Token %s" % args.token
    }
    # create user group
    usergroup_url = urljoin(args.url, USERGROUPS_ENDPOINT)
    usergroup_data = {"name": "example"}
    usergroup = find_or_create(usergroup_url, usergroup_data, headers)
    if usergroup is None:
        print("Usergroup not created")
        sys.exit(1)

    # create SQUAD group
    group_url = urljoin(args.url, GROUPS_ENDPOINT)
    group_data = {
        "name": "example",
        "slug": "example",
        "description": "Example group",
        "user_groups": [usergroup]}
    group = find_or_create(group_url, group_data, headers)
    if group is None:
        print("Group not created")
        sys.exit(1)

    # create SQUAD project
    project_url = urljoin(args.url, PROJECTS_ENDPOINT)
    project_data = {
        "name": "example",
        "slug": "example",
        "description": "Example project",
        "group": group,
        "is_public": True,
        "wait_before_notification": 3600,
        "notification_timeout": 36000,
        "moderate_notifications": False,
        "html_mail": True}
    project = find_or_create(project_url, project_data, headers)
    if project is None:
        print("Project not created")
        sys.exit(1)

    # create SQUAD LAVA CI backend
    backend_url = urljoin(args.url, BACKENDS_ENDPOINT)
    backend_data = {
        "name": urlparse(args.lava_url).netloc,
        "url": args.lava_url,
        "username": args.lava_user,
        "token": args.lava_token,
        "implementation_type": "lava",
        "backend_settings": "CI_LAVA_SEND_ADMIN_EMAIL: false\r\nCI_LAVA_HANDLE_SUITE: true",
        "poll_interval": 600,
        "max_fetch_attempts": 3,
        "poll_enabled": True}
    print(backend_data)
    backend = find_or_create(backend_url, backend_data, headers)
    if backend is None:
        print("Backend not created")
        sys.exit(1)


if __name__ == "__main__":
    main()
