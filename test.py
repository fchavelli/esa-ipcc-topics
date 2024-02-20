# Define the file path of your document
file_path = './data/reports/txt/wg1_ch11.txt'

# Initialize a counter for occurrences
occurrences = 0

# Open the file and read through it line by line
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Convert the line to lower case and count occurrences of 'precipitation'
        occurrences += line.lower().count('precipitation')

# Print the total number of occurrences
print(f"Total occurrences of 'precipitation': {occurrences}")