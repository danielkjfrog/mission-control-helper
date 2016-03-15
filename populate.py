import requests
import os
import re
from time import sleep
import json

def getInstancesUrls():
    artifactory_instances_map = {}
    regex = re.compile('^ARTIFACTORY(\d+)_PORT$')
    instances_keys = [instance for instance in os.environ if re.match(regex, instance)]
    for instance_key in instances_keys:
        instance_name = instance_key.replace("_PORT", "")
        instance_url = os.environ[instance_key].replace('tcp', 'http')
        artifactory_instances_map[instance_name] = instance_url
    return artifactory_instances_map

def getMissionControlUrl():
    regex = re.compile('^MISSIONCONTROL_PORT$')
    mc_key = [mc for mc in os.environ if re.match(regex, mc)]
    mission_control_url = os.environ[mc_key[0]].replace('tcp', 'http')
    return mission_control_url

def checkMissionControlUp():
    isUp = False
    while not isUp:
        try:
            if requests.get(getMissionControlUrl()).status_code == 200:
                print("Mission Control is Up!")
                isUp = True
        except requests.exceptions.ConnectionError:
            print("Waiting for Mission Control...")
            sleep(5)

def getMcToken():
    isToken = False
    while not isToken:
        try:
            mc_response = requests.post(getMissionControlUrl() +
                          "/api/ui/authentication", auth=("admin", "password"))
            if mc_response.status_code == 200:
                isToken = True
                mission_control_token = json.loads(mc_response.text)['data']
                return mission_control_token
        except requests.exceptions.ConnectionError:
            print("Waiting for Mission Control Token...")
            sleep(5)

def addInstances():
    token = getMcToken()
    for art_name, art_url in getInstancesUrls().iteritems():
        request_body = {"name": art_name, "url": art_url + "/artifactory",
                        "credentials": {"userName": "admin", "password": "password"}}
        auth_headers = {'Authorization': 'FE-TOKEN ' + token}
        create_instance = requests.post(getMissionControlUrl() + "/api/ui/instances",
                            headers=auth_headers, json=request_body)
        if create_instance.status_code == 201:
            print(art_name + " instance added to Mission Control.")
        else:
            print("Problem occurred adding " art_name + " instance to Mission Control.")

if __name__ == '__main__':
    getInstancesUrls()
    getMissionControlUrl()
    checkMissionControlUp()
    getMcToken()
    addInstances()
