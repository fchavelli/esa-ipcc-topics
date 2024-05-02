import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to extract chapter number from bib file name
def extract_chapter_number(bib_filename):
    return bib_filename.split('ch')[-1].split('.')[0]

# Function to check if DOI exists in bib file
def doi_exists_in_bib(doi, bib_content):
    return doi in bib_content

# Function to process each sheet in Excel file
def process_sheet(sheet_name, doi_column, folder_path):
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

# Function to process each sheet in Excel file and add 'Chapters' column
def process_excel(file_path, output_path, folder_path):
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
