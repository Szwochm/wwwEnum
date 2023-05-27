import json
import csv


# Function to read file names from a CSV file
def read_file_names(csv_file):
    file_names = set()
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if row:
                file_names.add(row[0])
    return file_names

# Function to compare versions
def compare_versions(version_csv1, version_csv2):
    file_names1 = read_file_names(version_csv1)
    file_names2 = read_file_names(version_csv2)

    file_names_missing_from_1 = file_names2 - file_names1
    file_names_missing_from_2 = file_names1 - file_names2

    differences = {
        "added_files": list(file_names_missing_from_2),
        "missing_files": list(file_names_missing_from_1)
    }

    return differences


# Read versions from versions.txt
with open('versions.txt', 'r') as file:
    versions = file.read().splitlines()

# Process each version
for version_csv in versions:
    output_dict = {}

    # Process current version
    current_files = read_file_names(version_csv)
    current_only_files = current_files.copy()

    # Compare with other versions
    for other_version_csv in versions:
        if other_version_csv != version_csv:
            differences = compare_versions(version_csv, other_version_csv)
            output_dict[other_version_csv] = differences
            current_only_files -= set(differences['added_files'])

    # Store results for current version
    current_results = {
        "added_files": [],
        "missing_files": list(current_only_files)
    }
    output_dict[version_csv] = current_results

    # Write differences to JSON file
    output_file = f"{version_csv.replace('.csv', '')}.json"
    with open(output_file, 'w') as file:
        json.dump(output_dict, file, indent=4)

    print(f"Differences for {version_csv} saved in {output_file}.")
