import csv
import json

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
        "version1": version_csv1,
        "version2": version_csv2,
        "missing_from_version1": list(file_names_missing_from_1),
        "missing_from_version2": list(file_names_missing_from_2)
    }

    return differences

# List of versions to compare
versions = [
    ("master.csv", "RELENG_2_5_1.csv"),
    ("RELENG_2_5_1.csv", "RELENG_2_4_5.csv"),
    ("RELENG_2_4_5.csv", "RELENG_2_4_4.csv"),
    ("RELENG_2_4_4.csv", "RELENG_2_4_3.csv"),
    ("RELENG_2_4_3.csv", "RELENG_2_4_2.csv"),
    ("RELENG_2_4_2.csv", "RELENG_2_4_1.csv"),
    ("RELENG_2_4_1.csv", "RELENG_2_4_0.csv"),
    ("RELENG_2_4_0.csv", "RELENG_2_3_5.csv"),
    ("RELENG_2_3_5.csv", "RELENG_2_3_4.csv"),
    ("RELENG_2_3_4.csv", "RELENG_2_3_3.csv"),
    ("RELENG_2_3_3.csv", "RELENG_2_3_2.csv"),
    ("RELENG_2_3_2.csv", "RELENG_2_3_1.csv"),
    ("RELENG_2_3_1.csv", "RELENG_2_3_0.csv"),
    ("RELENG_2_3_0.csv", "RELENG_2_2.csv"),
    ("RELENG_2_2.csv", "RELENG_2_1.csv"),
    ("RELENG_2_1.csv", "RELENG_2_0.csv"),
    ("RELENG_2_0.csv", "RELENG_1_2.csv")
]

# Output file to store all differences
output_file = "differences_versions.json"

differences_list = []
for version1, version2 in versions:
    differences = compare_versions(version1, version2)
    differences_list.append(differences)

# Write differences to JSON file
with open(output_file, 'w') as file:
    json.dump(differences_list, file, indent=4)

print(f"Differences between versions saved in {output_file}.")
