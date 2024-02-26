import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
import json
from env_config import JFROG_URL, JFROG_USER, JFROG_PASSWORD

# Initialize session
session = requests.Session()
session.auth = HTTPBasicAuth(JFROG_USER, JFROG_PASSWORD)

def list_packages(repo_name):
    # Generalized AQL query without specifying file extension
    aql_query = json.dumps({
        "repo": repo_name,
        "type": "file",
    })
    response = session.post(f"{JFROG_URL}/api/search/aql", data='items.find(' + aql_query + ')', headers={"Content-Type": "text/plain"})
    package_list = []
    if response.status_code == 200:
        results = response.json().get('results', [])
        for item in results:
            package_url = urljoin(JFROG_URL, f"artifactory/{item['repo']}/{item['path']}/{item['name']}")
            package_list.append(package_url)
    else:
        print(f"Failed to list packages in {repo_name}: {response.status_code}, Response: {response.text}")
    return package_list