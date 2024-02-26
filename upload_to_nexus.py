import requests
from env_config import NEXUS_URL, NEXUS_USER, NEXUS_PASSWORD, JFROG_URL, JFROG_USER, JFROG_PASSWORD
from requests.auth import HTTPBasicAuth

# Configure session for Nexus
nexus_session = requests.Session()
nexus_session.auth = HTTPBasicAuth(NEXUS_USER, NEXUS_PASSWORD)
# Consider enabling SSL verification and providing the path to your CA bundle here
# nexus_session.verify = '/path/to/ca_bundle'

# Configure session for JFrog
jfrog_session = requests.Session()
jfrog_session.auth = HTTPBasicAuth(JFROG_USER, JFROG_PASSWORD)

def file_exists_in_nexus(repo_name, file_path):
    """Check if a file already exists in the Nexus repository"""
    nexus_file_url = f"{NEXUS_URL}/repository/{repo_name}/{file_path}"
    response = nexus_session.head(nexus_file_url)
    return response.status_code == 200

def download_file_from_jfrog(file_url):
    """Download a file from JFrog Artifactory"""
    response = jfrog_session.get(file_url, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download file from JFrog: {response.status_code}")

def upload_file_to_nexus(repo_name, file_path, file_content, content_type='application/octet-stream'):
    """Upload a file to a Nexus repository"""
    if file_content is None:
        raise ValueError("No file content to upload.")
    nexus_file_url = f"{NEXUS_URL}/repository/{repo_name}/{file_path}"
    headers = {'Content-Type': content_type}
    response = nexus_session.put(nexus_file_url, data=file_content, headers=headers)
    if response.status_code in [200, 201]:
        print(f"Successfully uploaded {file_path} to Nexus.")
    else:
        raise Exception(f"Failed to upload {file_path} to Nexus: {response.status_code}, {response.text}")

def upload_to_nexus(repo_name, repo_type, package_list):
    """Upload package list from JFrog to Nexus"""
    for file_url in package_list:
        file_path = '/'.join(file_url.split('/')[len(JFROG_URL.split('/')):])
        if not file_exists_in_nexus(repo_name, file_path):
            file_content = download_file_from_jfrog(file_url)
            # Example to handle different content types, adjust as needed
            if repo_type == 'maven':
                content_type = 'application/xml'
            elif repo_type in ['yum', 'apt']:
                content_type = 'application/x-rpm'
            else:
                content_type = 'application/octet-stream'
            upload_file_to_nexus(repo_name, file_path, file_content, content_type)
        else:
            print(f"File {file_path} already exists in Nexus, skipping.")
