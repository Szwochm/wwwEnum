import json
import requests
import time

def get_directory_contents(owner, repo, branch, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    response = requests.get(url)
    
    if response.status_code == 200:
        contents = response.json()
        file_names = [item['name'] for item in contents if item['type'] == 'file']
        directory_names = [item['name'] for item in contents if item['type'] == 'dir']
        return file_names, directory_names
    else:
        return None, None

owner = "pfsense"
repo = "pfsense"
branches = [
    "RELENG_1_2",
    "RELENG_2_0",
    "RELENG_2_1",
    "RELENG_2_2"
]
path = "usr/local/www"
delay = 3  # Delay in seconds between requests

all_data = {}

for branch in branches:
    file_names, directory_names = get_directory_contents(owner, repo, branch, path)

    if file_names is None or directory_names is None:
        print(f"Failed to fetch directory contents for branch {branch}.")
        continue

    version = branch.replace('/', '_')
    all_data[version] = {
        "file_names": file_names,
        "directory_names": directory_names
    }

    time.sleep(delay)

json_file = "directory_contents.json"
with open(json_file, 'w') as file:
    json.dump(all_data, file, indent=4)

print(f"All directory contents saved in {json_file}.")
