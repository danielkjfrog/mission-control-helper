import requests
import os
import re

def getInstancesUrls():
    regex = re.compile('ARTIFACTORY\d+_PORT=tcp:\/\/\d+.\d+.\d+.\d+:\d+')
    instances_keys = [instance for instance in os.environ if re.match(regex, instance)]
    instances_urls = [os.environ[instance_key].replace('tcp', 'http') for instance_key in instances_keys]
    return instances_urls

def getMissionControlUrl():
    pass

if __name__ == '__main__':
    print(getInstancesUrls())
