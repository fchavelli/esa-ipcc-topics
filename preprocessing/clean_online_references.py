import os
import re
import openpyxl
import pandas as pd

def remove_starting_sequence(value):
    pattern = r'^\d{1,4}\.\s'
    return re.sub(pattern, '', value)

def process_xlsx_file(input_file, output_file):
    wb = openpyxl.load_workbook(input_file)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=1, max_col=1):
        cell = row[0]
        if cell.value:
            cell.value = remove_starting_sequence(cell.value)

    wb.save(output_file)

def remove_empty_rows(input_file, output_file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_file)

    # Remove empty rows
    df.dropna(axis=0, how='all', inplace=True)

    # Save the DataFrame to a new Excel file
    df.to_excel(output_file, index=False)

def remove_duplicates(input_file, output_file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(input_file)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Save the DataFrame to a new Excel file
    df.to_excel(output_file, index=False)

# Create directories if they don't exist
directory = "./data/online_references"

for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory, filename)
        process_xlsx_file(file_path, file_path)
        remove_empty_rows(file_path, file_path)
        remove_duplicates(file_path, file_path)
