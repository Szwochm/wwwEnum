import requests

# Set the repository information
owner = 'pfsense'
repo = 'pfsense'

# Make the API request to get the branches
url = f'https://api.github.com/repos/{owner}/{repo}/branches'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    branches = response.json()

    # Extract the branch names
    branch_names = [branch['name'] for branch in branches]

    # Save branch names to versions.txt
    with open('versions.txt', 'w') as file:
        file.write('\n'.join(branch_names))

    print("Branch names saved to versions.txt file.")
else:
    print(f"Failed to retrieve branch names. Status Code: {response.status_code}")
