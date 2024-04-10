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
input_file = './results/dois/ar6_dois_wg2.txt'  # Replace 'input.txt' with your input file name
output_file = './results/dois/ar6_dois_wg2_no_duplicates.txt'  # Replace 'output.txt' with your desired output file name

remove_duplicates(input_file, output_file)
