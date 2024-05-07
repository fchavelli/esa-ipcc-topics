"""
This script provides functions to process bibliographic references in .bib format.
It can read a .bib file, filter entries based on DOIs, create Excel sheets for specific tags,
and save matching entries to new .bib files.

Functions:
- read_bib_file(filepath): Read a .bib file and return its content.
- find_files_with_tag(folder_path, tag): Find all .bib files in the given folder that contain the tag in their name.
- filter_entries_by_doi(bib_database, dois): Filter entries in a bib_database that have a DOI matching any in the list 'dois'.
- create_excel_sheet(writer, tag, entries): Create an Excel sheet for the given tag with the provided entries.
- process_files(folder_path, original_bib_path, report_tags): Process the .bib files in the specified folder based on the given tags.

Example usage:
folder_path = './data/references_no_duplicates'
original_bib_path = './data/cci/cci_papers_merged.bib'
report_tags = ['sr15', 'srccl', 'srocc', 'wg1', 'wg2', 'wg3']

process_files(folder_path, original_bib_path, report_tags)
"""

import os
import logging
import bibtexparser
import pandas as pd

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def read_bib_file(filepath):
    """Read a .bib file and return its content."""
    try:
        with open(filepath, encoding='utf8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        return bib_database
    except Exception as e:
        logging.error(f"Error reading {filepath}: {e}")
        return None

def find_files_with_tag(folder_path, tag):
    """Find all .bib files in the given folder that contain the tag in their name."""
    tagged_files = [f for f in os.listdir(folder_path) if f.endswith('.bib') and tag in f]
    return tagged_files

def filter_entries_by_doi(bib_database, dois):
    """Filter entries in a bib_database that have a DOI matching any in the list 'dois'."""
    filtered_entries = [entry for entry in bib_database.entries if entry.get('doi') in dois]
    return filtered_entries

def create_excel_sheet(writer, tag, entries):
    """Create an Excel sheet for the given tag with the provided entries."""
    # Convert entries to a DataFrame
    df = pd.DataFrame(entries, columns=['Project', 'DOI', 'Title', 'Year', 'Author', 'Journal'])
    df.to_excel(writer, sheet_name=tag, index=False)

def process_files(folder_path, original_bib_path, report_tags):
    original_bib_db = read_bib_file(original_bib_path)
    if not original_bib_db:
        logging.error("Failed to read the original bib file. Exiting...")
        return

    original_dois = {entry.get('doi') for entry in original_bib_db.entries if entry.get('doi')}

    # Initialize Excel writer
    excel_writer = pd.ExcelWriter('./results/matched_references.xlsx', engine='openpyxl')

    for tag in report_tags:
        logging.info(f"Processing tag: {tag}")
        tagged_files = find_files_with_tag(folder_path, tag)
        if not tagged_files:
            logging.info(f"No files found for {tag} report. Continuing to next report...")
            continue

        # Collect DOIs from files with the current tag
        tag_dois = set()
        for file in tagged_files:
            logging.info(f"Analysing file: {file}")
            db = read_bib_file(os.path.join(folder_path, file))
            if db:
                tag_dois.update(entry.get('doi') for entry in db.entries if entry.get('doi'))

        # Filter original entries by DOIs found in tagged files
        matching_entries = filter_entries_by_doi(original_bib_db, tag_dois)

        if matching_entries:
            # Write these entries to a new .bib file named after the tag
            new_bib_db = bibtexparser.bibdatabase.BibDatabase()
            new_bib_db.entries = matching_entries
            with open(f"./results/matched_references_{tag}.bib", 'w', encoding='utf8') as new_bib_file:
                bibtexparser.dump(new_bib_db, new_bib_file)
            logging.info(f"Created matched_references_{tag}.bib with {len(matching_entries)} entries.")

            # Prepare data for Excel
            excel_entries = []
            for entry in matching_entries:
                excel_entries.append({
                    'Project': entry.get('project', ''),  # Use the 'project' field from the entry
                    'DOI': entry.get('doi', ''),
                    'Title': entry.get('title', ''),
                    'Year': entry.get('year', ''),
                    'Author': entry.get('author', ''),
                    'Journal': entry.get('journal', '')
                })
            
            # Create Excel sheet for the tag
            create_excel_sheet(excel_writer, tag, excel_entries)
        else:
            logging.info(f"No matching entries found for {tag} report.")

    # Correctly save and close the Excel file
    excel_writer.close()

# Example usage
folder_path = './data/references_no_duplicates'
original_bib_path = './data/cci/cci_papers_merged.bib'
report_tags = ['sr15', 'srccl', 'srocc', 'wg1', 'wg2', 'wg3']

process_files(folder_path, original_bib_path, report_tags)
