def remove_duplicates(input_file, output_file):
    # Read lines from input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Remove duplicates
    unique_lines = list(set(lines))

    # Write unique lines to output file
    with open(output_file, 'w') as f:
        f.writelines(unique_lines)

# Example usage
input_file = 'input.txt'  # Replace 'input.txt' with your input file name
output_file = 'output.txt'  # Replace 'output.txt' with your desired output file name

remove_duplicates(input_file, output_file)
