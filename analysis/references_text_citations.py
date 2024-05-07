"""
This script processes an Excel workbook containing information about references and their associated chapters.
It searches for specific patterns in text files and counts the occurrences of those patterns.
Note that the specific patterns are limited to ([First Author] et al., [Year]) format.
Note that the count is set to 1 by default because each paper is cited at least once (as present in chapter bib files).
The results are then added to the workbook and saved as a new Excel file.

Functions:
- create_search_pattern(author, year): Creates a regex pattern for searching based on the author and year.
- count_pattern_in_file(file_path, pattern): Counts the occurrences of a pattern in a text file.
- process_workbook(file_path, output_path, data_folder): Processes the workbook, counts the pattern occurrences, and saves the modified workbook.

Usage:
- Modify the file_path, output_path, and data_folder variables according to your file locations.
- Call the process_workbook function with the appropriate arguments.
"""

import pandas as pd
import os
import re

def create_search_pattern(author, year):
    """
    Creates a regex pattern for searching based on the author and year.

    Args:
    - author (str): The author's name.
    - year (str): The publication year.

    Returns:
    - pattern (re.Pattern): The compiled regex pattern.
    """
    normalized_author = re.escape(author)
    pattern = f"{normalized_author}\\s*et\\s*al.,\\s*{year}"
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE)

def count_pattern_in_file(file_path, pattern):
    """
    Counts the occurrences of a pattern in a text file.

    Args:
    - file_path (str): The path to the text file.
    - pattern (re.Pattern): The compiled regex pattern.

    Returns:
    - count (int): The number of occurrences of the pattern in the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        count = len(pattern.findall(content))
        return max(1, count)  # Ensure that count is at least 1
    except FileNotFoundError:
        return 1  # Return 1 if the file is not found

def process_workbook(file_path, output_path, data_folder):
    """
    Processes the workbook, counts the pattern occurrences, and saves the modified workbook.

    Args:
    - file_path (str): The path to the input Excel file.
    - output_path (str): The path to save the modified Excel file.
    - data_folder (str): The folder containing the text files to search.

    Returns:
    - output_path (str): The path to the saved modified Excel file.
    """
    workbook = pd.ExcelFile(file_path)
    writer = pd.ExcelWriter(output_path)

    # Process each sheet in the workbook
    for sheet_name in workbook.sheet_names:
        print("Processing sheet:", sheet_name)
        df = workbook.parse(sheet_name)
        # Initialize new columns
        df['File Counts'] = ''
        df['Total Count'] = 0

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            first_author = row['First Author']
            year = row['Year']
            chapters = str(row['Chapters']).split(';')  # Convert to string to handle unexpected types
            file_counts = []
            total_count = 0

            # Regex pattern for the current author and year
            pattern = create_search_pattern(first_author, year)

            # Process each chapter
            for chapter in chapters:
                file_id = f"{sheet_name}_ch{chapter.strip()}"
                file_path = os.path.join(data_folder, f"{file_id}.txt")
                count = count_pattern_in_file(file_path, pattern)
                file_counts.append(f"{chapter.strip()}:{count}")
                total_count += count

            # Update the DataFrame with the counts
            df.at[index, 'File Counts'] = ';'.join(file_counts)
            df.at[index, 'Total Count'] = total_count

        # Write updated DataFrame to new sheet in the output Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Save the modified workbook
    writer._save()
    print('Processing completed. Output file saved to:', output_path)
    return output_path

# Usage of the function
file_path = './data/cci/matched_references_unique_formated.xlsx'
output_path = './results/matched_references_number_of_citations.xlsx'
data_folder = './data/reports/content'
process_workbook(file_path, output_path, data_folder)
