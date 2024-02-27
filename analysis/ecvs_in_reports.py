import logging
import os
import re
import json
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Load search terms and their aliases
with open('./data/cci/ecv_aliases.json', 'r') as f:
    ecv_aliases = json.load(f)

search_terms = ecv_aliases

# Directory containing .txt files
directory_path = './data/reports/txt'
directory_path = './temp'

# Prepare regex patterns for search terms
patterns = {}
for term, aliases in search_terms.items():
    all_terms = [term] + aliases
    pattern = '|'.join(re.escape(alias) for alias in all_terms)
    patterns[term] = re.compile(pattern, re.IGNORECASE)

# Define tags
tags = ['sr15', 'srccl', 'srocc', 'wg1', 'wg2', 'wg3', 'syr']

# Function to extract tag from filename
def extract_tag(filename, tags):
    for tag in tags:
        if tag in filename:
            return tag
    return 'other'

# Group files by tag
files_by_tag = {}
for file in os.listdir(directory_path):
    if file.endswith('.txt'):
        tag = extract_tag(file, tags)
        if tag not in files_by_tag:
            files_by_tag[tag] = []
        files_by_tag[tag].append(file)

# Initialize Excel writer
excel_path = './results/ecvs_in_reports.xlsx'
excel_path = './temp/ecvs_in_reports.xlsx'
with pd.ExcelWriter(excel_path) as writer:
    for tag, files in files_by_tag.items():
        # Initialize DataFrame for the current tag
        results_df = pd.DataFrame(columns=['ECV'] + [file.replace('.txt', '') for file in files])
        results_df['ECV'] = list(search_terms.keys())

        # Search through files of the current tag
        for file in files:
            logging.info(f'Processing file: {file}')
            try:
                with open(os.path.join(directory_path, file), 'r', encoding='utf-8') as f:
                    text = f.read()
                for term, pattern in patterns.items():
                    count = len(pattern.findall(text))
                    results_df.loc[results_df['ECV'] == term, file.replace('.txt', '')] = count
            except Exception as e:
                logging.warning(f'Error processing file {file}: {e}')

        # Write results of the current tag to a separate sheet in the Excel document
        results_df.to_excel(writer, sheet_name=tag, index=False)

# Log completion
logging.info(f'Results written to {excel_path}')
logging.info('Search completed. Check the logs for any warnings or errors.')
