import csv
import requests
import time
import os

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

# Read branches from versions.txt
with open('versions.txt', 'r') as file:
    branches = file.read().splitlines()

delay = 1  # Delay in seconds between requests

for branch in branches:
    version = branch.replace('/', '_')
    csv_file = f"{version}.csv"
    
    if os.path.exists(csv_file):
        print(f"CSV file {csv_file} already exists. Skipping.")
        continue
    
    path = "src/usr/local/www"
    
    file_names, directory_names = get_directory_contents(owner, repo, branch, path)

    if file_names is None or directory_names is None:
        print(f"Failed to fetch directory contents for branch {branch}.")
        continue

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
