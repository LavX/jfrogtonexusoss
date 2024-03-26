import requests
import logging
from create_repo_nexus import repo_exists, create_repo
from env_config import NEXUS_URL, NEXUS_USER, NEXUS_PASSWORD, JFROG_URL, JFROG_USER, JFROG_PASSWORD
from requests.auth import HTTPBasicAuth

# Configure session for Nexus
nexus_session = requests.Session()
nexus_session.auth = HTTPBasicAuth(NEXUS_USER, NEXUS_PASSWORD)
# Consider enabling SSL verification and providing the path to your CA bundle here
# nexus_session.verify = '/path/to/ca_bundle'

# Initialize logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


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
    try:
        response = jfrog_session.get(file_url, stream=True)
        if response.status_code == 200:
            return response.content
        else:
            logging.error(f"Failed to download file from JFrog: {response.status_code} - URL: {file_url}")
            return None
    except Exception as e:
        logging.error(f"Exception during file download from JFrog: {e} - URL: {file_url}")
        return None
    
def ensure_repo_exists(repo_name, repo_type):
    if not repo_exists(repo_name):
        create_repo(repo_name, repo_type)
    else:
        print(f"Repository {repo_name} already exists.")

def upload_file_to_nexus(repo_name, file_path, file_content, content_type='application/octet-stream'):
    """Upload a file to a Nexus repository"""
    nexus_file_url = f"{NEXUS_URL}/repository/{repo_name}/{file_path}"
    headers = {'Content-Type': content_type}
    response = None 
    try:
        response = nexus_session.put(nexus_file_url, data=file_content, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Successfully uploaded {file_path} to Nexus.")
        else:
            print(f"Failed to upload {file_path} to Nexus: {response.status_code}, {response.text}")
            logging.error(f"Failed to upload {file_path} to Nexus: {response.status_code}, {response.text}")
    except Exception as e:
        error_message = f"Exception during file upload to Nexus: {e} - URL: {nexus_file_url}"
        print(error_message)
        logging.error(error_message)

def upload_to_nexus(repo_name, repo_type, package_list):
    """Upload package list from JFrog to Nexus"""
    ensure_repo_exists(repo_name, repo_type)
    for file_url in package_list:
        file_path = '/'.join(file_url.split('/')[len(JFROG_URL.split('/')):])[len(repo_name)+1:]
        if not file_exists_in_nexus(repo_name, file_path):
            file_content = download_file_from_jfrog(file_url)
            if repo_type == 'maven':
                content_type = 'application/xml'
            elif repo_type in ['yum', 'apt']:
                content_type = 'application/x-rpm'
            else:
                content_type = 'application/octet-stream'
            upload_file_to_nexus(repo_name, file_path, file_content, content_type)
        else:
            print(f"File {file_path} already exists in Nexus, skipping.")