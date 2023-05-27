import glob
import csv

# Find all CSV files in the current directory
csv_files = glob.glob('*.csv')

# Set to store all filenames and directory names
names_set = set()

# Process each CSV file
for csv_file in csv_files:
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for item in row:
                names_set.add(item)

# Create a text file and write the names
with open('wordlist.txt', 'w') as file:
    for name in sorted(names_set):
        file.write(name + '\n')
