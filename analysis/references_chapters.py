"""
This script processes an Excel file containing multiple sheets and adds a 'Chapters' column to each sheet.
The 'Chapters' column is populated by searching for chapter numbers in corresponding .bib files.

The script contains the following functions:
- extract_chapter_number(bib_filename): Extracts the chapter number from a .bib file name.
- doi_exists_in_bib(doi, bib_content): Checks if a DOI exists in the content of a .bib file.
- process_sheet(sheet_name, doi_column, folder_path): Processes each sheet in the Excel file
  and returns a comma-separated string of chapter numbers found in the corresponding .bib files.
- process_excel(file_path, output_path, folder_path): Processes each sheet in the Excel file,
  adds the 'Chapters' column, and saves the updated Excel file.

Example usage:
- input_excel_path: Path to the input Excel file.
- output_excel_path: Path to save the output Excel file.
- bib_folder_path: Path to the folder containing the .bib files.

Note: This script requires the pandas library to be installed.
"""

import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_chapter_number(bib_filename):
    """
    Extracts the chapter number from a .bib file name.

    Args:
        bib_filename (str): The name of the .bib file.

    Returns:
        str: The extracted chapter number.
    """
    return bib_filename.split('ch')[-1].split('.')[0]

def doi_exists_in_bib(doi, bib_content):
    """
    Checks if a DOI exists in the content of a .bib file.

    Args:
        doi (str): The DOI to check.
        bib_content (str): The content of the .bib file.

    Returns:
        bool: True if the DOI exists, False otherwise.
    """
    return doi in bib_content

def process_sheet(sheet_name, doi_column, folder_path):
    """
    Processes each sheet in the Excel file and returns a comma-separated string of chapter numbers found in the corresponding .bib files.

    Args:
        sheet_name (str): The name of the sheet.
        doi_column (str): The name of the DOI column in the sheet.
        folder_path (str): The path to the folder containing the .bib files.

    Returns:
        str: A comma-separated string of chapter numbers found in the .bib files.
    """
    bib_files = [file for file in os.listdir(folder_path) if file.endswith('.bib') and sheet_name in file]

    chapters = []

    for bib_file in bib_files:
        with open(os.path.join(folder_path, bib_file), 'r', encoding='utf8') as file:
            bib_content = file.read()
            if doi_exists_in_bib(doi_column, bib_content):
                chapter_number = extract_chapter_number(bib_file)
                logger.info(f'Found chapter {chapter_number} in bib file {bib_file}')
                chapters.append(chapter_number)

    return ','.join(chapters) if chapters else None

def process_excel(file_path, output_path, folder_path):
    """
    Processes each sheet in the Excel file, adds the 'Chapters' column, and saves the updated Excel file.

    Args:
        file_path (str): The path to the input Excel file.
        output_path (str): The path to save the output Excel file.
        folder_path (str): The path to the folder containing the .bib files.
    """
    df = pd.read_excel(file_path, sheet_name=None)
    writer = pd.ExcelWriter(output_path)

    total_sheets = len(df)
    current_sheet = 0

    for sheet_name, sheet_data in df.items():
        current_sheet += 1
        logger.info(f'Processing sheet {current_sheet}/{total_sheets}: {sheet_name}')
        try:
            sheet_data['Chapters'] = sheet_data.apply(lambda row: process_sheet(sheet_name, row['DOI'], folder_path), axis=1)
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)
        except Exception as e:
            logger.error(f'Error processing sheet {sheet_name}: {e}')

    writer._save()

# Example usage
input_excel_path = './results/matched_references.xlsx'
output_excel_path = './results/matched_references_refined.xlsx'
bib_folder_path = './data/references_no_duplicates'

logger.info('Starting processing...')
process_excel(input_excel_path, output_excel_path, bib_folder_path)
logger.info('Processing complete.')
