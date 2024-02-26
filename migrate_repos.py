import sys
import json
from scan_source import scan_all_repositories
from list_packages import list_packages
from upload_to_nexus import upload_to_nexus
from env_config import *

def read_config():
    with open('config.json') as config_file:
        return json.load(config_file)

def main():
    use_config = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == "scanall":
        use_config = False

    if use_config:
        config = read_config()
    else:
        config = scan_all_repositories()

    for repo in config:
        package_list = list_packages(repo['name'])
        upload_to_nexus(repo['name'], repo['type'], package_list)

if __name__ == "__main__":
    main()
