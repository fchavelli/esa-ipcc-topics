import logging
import os
import re
import json
import pandas as pd

# To do: modify the count to exclude occurences from in text references
# Subtract occurences in references titles, not in all .bib file (to ignore abstracts)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Load search terms and their aliases
with open('./data/cci/ecv_aliases.json', 'r') as f:
    search_terms = json.load(f)

# Directory containing .txt files
directory_path = './data/reports/content'
output_excel_path = './results/ecvs_in_reports.xlsx'  # Actual output file path

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
excel_path_temp = './results/ecvs_in_reports_temp.xlsx'

with pd.ExcelWriter(excel_path_temp) as writer:
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

# Sort the columns so that CH10 appears after CH9 and not after CH1
def sort_columns(df):
    ecv_column = df['ECV'] if 'ECV' in df.columns else None
    def sort_key(col):
        if 'ch' in col:
            num_part = int(''.join(filter(str.isdigit, col.split('ch')[-1])))
            return (0, num_part)
        elif 'a' not in col:
            return (1, col)
        else:
            return (2, col)
    columns_to_sort = [col for col in df.columns if col != 'ECV']
    sorted_columns = sorted(columns_to_sort, key=sort_key)
    if ecv_column is not None:
        sorted_columns = ['ECV'] + sorted_columns
    return df[sorted_columns]

input_excel_path = excel_path_temp  # Actual input file path

with pd.ExcelWriter(output_excel_path) as writer:
    for sheet_name in pd.ExcelFile(input_excel_path).sheet_names:
        df = pd.read_excel(input_excel_path, sheet_name=sheet_name)
        df_sorted = sort_columns(df)
        df_sorted.to_excel(writer, sheet_name=sheet_name, index=False)

# Check if the file exists and then remove it
if os.path.exists(excel_path_temp):
    os.remove(excel_path_temp)
else:
    print("Temporary file does not exist.")

# Log completion
logging.info(f'Results written to {output_excel_path}')
logging.info('Search completed. Check the logs for any warnings or errors.')