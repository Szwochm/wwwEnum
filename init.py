import csv
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

for branch in branches:
    file_names, directory_names = get_directory_contents(owner, repo, branch, path)

    if file_names is None or directory_names is None:
        print(f"Failed to fetch directory contents for branch {branch}.")
        continue

    version = branch.replace('/', '_')
    csv_file = f"{version}.csv"

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Names"])
        for file in file_names:
            writer.writerow([file])
        
        writer.writerow([])  # Empty row separator
        
        writer.writerow(["Directory Names"])
        for directory in directory_names:
            writer.writerow([directory])

    print(f"Directory contents for branch {branch} stored in {csv_file}.")
    time.sleep(delay)
