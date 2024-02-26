import requests
from env_config import JFROG_URL, JFROG_USER, JFROG_PASSWORD
from requests.auth import HTTPBasicAuth

session = requests.Session()
session.auth = HTTPBasicAuth(JFROG_USER, JFROG_PASSWORD)

def scan_all_repositories():
    """Scan all repositories from JFrog using configurations endpoint and return their names and types."""
    configurations_url = f"{JFROG_URL}/api/repositories/configurations"
    response = session.get(configurations_url, verify=True)  # Use verify=True in production for SSL verification
    repositories = []
    if response.status_code == 200:
        configurations = response.json()
        for repo_type, repos in configurations.items():
            for repo in repos:
                # Extract repository type and map it accordingly
                artifactory_type = repo.get('packageType').lower()
                # Example mapping, adjust based on your requirements
                if artifactory_type == "rpm":
                    nexus_type = "rpm"
                elif artifactory_type == "debian":
                    nexus_type = "debian"
                elif artifactory_type == "maven" or artifactory_type == "buildinfo":
                    nexus_type = "maven"
                else:
                    nexus_type = artifactory_type  # Use the Artifactory type directly if no mapping is needed

                repositories.append({"name": repo['key'], "type": nexus_type, "artifactoryType": repo_type.lower()})
    else:
        print(f"Failed to scan repositories: {response.status_code}, Message: {response.text}")
    return repositories
