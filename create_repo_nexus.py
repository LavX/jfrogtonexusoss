import requests
from env_config import NEXUS_URL, NEXUS_USER, NEXUS_PASSWORD
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.auth = HTTPBasicAuth(NEXUS_USER, NEXUS_PASSWORD)

def repo_exists(repo_name):
    print(f"Checking if {repo_name} repository exists in Nexus.")
    """Check if the repository exists in Nexus."""
    response = session.get(f"{NEXUS_URL}/service/rest/v1/repositories")
    if response.ok:
        for repo in response.json():
            if repo['name'] == repo_name:
                return True
    else:
        print(f"Error checking repository existence: {response.status_code}")
    return False

def create_repo(repo_name, repo_type):
    """Create a repository in Nexus if it doesn't exist and if the type is supported."""
    if repo_exists(repo_name):
        print(f"Repository {repo_name} already exists.")
        return

    supported_types = ['rpm', 'debian', 'maven']
    if repo_type not in supported_types:
        print(f"Skipping creation of {repo_name}. Unsupported repository type: {repo_type}")
        return  # Skip creation for unsupported types

    headers = {'Content-Type': 'application/json'}
    data = {
        "name": repo_name,
        "online": True,
        "storage": {
            "blobStoreName": "default",
            "strictContentTypeValidation": True,
            "writePolicy": "allow_once"  # Added based on the working curl example
        }
    }

    # Adjusting data structure based on repo_type
    if repo_type == "rpm":
        data.update({
            "recipe": "yum-hosted",
            "format": "yum"
        })
        post_url = f"{NEXUS_URL}/service/rest/v1/repositories/yum-hosted"
    elif repo_type == "debian":
        data.update({
            "recipe": "apt-hosted",
            "format": "apt"
        })
        post_url = f"{NEXUS_URL}/service/rest/v1/repositories/apt-hosted"
    elif repo_type == "maven":
        data.update({
            "recipe": "maven2-hosted",
            "format": "maven2",
            "maven": {
                "versionPolicy": "RELEASE",
                "layoutPolicy": "STRICT"
            }
        })
        # Use a fixed URL structure for Maven to match the working curl example
        post_url = f"{NEXUS_URL}/service/rest/v1/repositories/maven/hosted"

    response = session.post(post_url, json=data, headers=headers)
    if response.ok:
        print(f"Successfully created {repo_name} repository.")
    else:
        print(f"Failed to create {repo_name} repository. Status: {response.status_code}, Response: {response.text}")
