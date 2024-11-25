import csv

# Initialize an empty dictionary
data_dict = {}

# Open the CSV file
with open('materialcas.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    
    # Skip the header row if needed
    next(csv_reader)
    
    # Iterate through the CSV rows
    for row in csv_reader:
        # Use the first column as the key and the second column as the value
        data_dict[row[0]] = row[1]

print(data_dict)
