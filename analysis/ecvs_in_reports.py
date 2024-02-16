import logging
import os
import re
import json
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Define search terms and their aliases

with open('./data/cci/ecv_aliases.json', 'r') as f:
    ecv_aliases = json.load(f)

search_terms = ecv_aliases

# Directory containing .txt files
directory_path = './data/reports/txt'

# Prepare regex patterns for search terms
patterns = {}
for term, aliases in search_terms.items():
    all_terms = [term] + aliases
    pattern = '|'.join(re.escape(alias) for alias in all_terms)
    patterns[term] = re.compile(pattern, re.IGNORECASE)

# DataFrame to store results
results_df = pd.DataFrame(columns=['ECV'] + [file.replace('.txt', '') for file in os.listdir(directory_path) if file.endswith('.txt')])
results_df['ECV'] = list(search_terms.keys())

# Search through files
for file in os.listdir(directory_path):
    if file.endswith('.txt'):
        logging.info(f'Processing file: {file}')
        try:
            with open(os.path.join(directory_path, file), 'r', encoding='utf-8') as f:
                text = f.read()
            for term, pattern in patterns.items():
                count = len(pattern.findall(text))
                results_df.loc[results_df['ECV'] == term, file.replace('.txt', '')] = count
        except Exception as e:
            logging.warning(f'Error processing file {file}: {e}')

# Write results to Excel
excel_path = './results/ecvs_in_reports.xlsx'
results_df.to_excel(excel_path, index=False)
logging.info(f'Results written to {excel_path}')

# Summary
logging.info('Search completed. Check the logs for any warnings or errors.')
