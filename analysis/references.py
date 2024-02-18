import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Documentation
"""
This script finds common references based on DOIs across multiple BibTeX files in a specified folder and compiles them into a new BibTeX file.
- Parses each .bib file in the folder to find DOIs.
- Compares DOIs across all files to find matches.
- Writes matched references to a new file, ensuring no duplicates.
- Logs progress and provides a summary of the analysis.
"""

def parse_bib_file(file_path):
    """Parse a BibTeX file and return the database object."""
    try:
        with open(file_path, encoding='utf-8') as bibtex_file:
            parser = BibTexParser(common_strings=True)
            parser.customization = convert_to_unicode
            bib_database = bibtexparser.load(bibtex_file, parser=parser)
        return bib_database
    except Exception as e:
        logging.error(f"Error parsing file {file_path}: {e}")
        return None

def find_common_references(main_bib_file, folder_path):
    """Find common references across BibTeX files and compile them into a new file."""
    main_db = parse_bib_file(main_bib_file)
    if not main_db:
        logging.error("Failed to parse main BibTeX file.")
        return

    main_dois = {entry.get('doi', '').lower() for entry in main_db.entries if 'doi' in entry}
    matched_entries = []
    files_analyzed = 0

    for file in tqdm(os.listdir(folder_path), desc="Analyzing files"):
        if file.endswith(".bib") and file != os.path.basename(main_bib_file) and 'wg1_ch' in file:
            file_path = os.path.join(folder_path, file)
            current_db = parse_bib_file(file_path)
            if not current_db:
                continue  # Skip files that couldn't be parsed
            
            current_dois = {entry.get('doi', '').lower() for entry in current_db.entries if 'doi' in entry}
            common_dois = main_dois.intersection(current_dois)
            
            for entry in main_db.entries:
                if entry.get('doi', '').lower() in common_dois:
                    if entry not in matched_entries:  # Avoid duplicates
                        matched_entries.append(entry)
            
            files_analyzed += 1

    # Writing matched entries to a new file
    if matched_entries:
        try:
            matched_db = bibtexparser.bibdatabase.BibDatabase()
            matched_db.entries = matched_entries
            
            with open('./results/matched_references.bib', 'w', encoding='utf-8') as bibtex_file:
                bibtexparser.dump(matched_db, bibtex_file)
                
            logging.info(f"Matched references written to 'matched_references.bib'.")
        except Exception as e:
            logging.error(f"Failed to write matched references: {e}")
    
    # Summary
    logging.info(f"Files analyzed: {files_analyzed}")
    logging.info(f"Matched references found: {len(matched_entries)}")
    logging.info(f"Unique DOIs (avoided duplicates): {len(set([entry['doi'] for entry in matched_entries if 'doi' in entry]))}")


# Example usage
main_bib_file = './data/references/cci_no_duplicates.bib' # Replace with the path to your main BibTeX file
folder_path = './data/references' # Replace with the path to your folder containing BibTeX files
exlude_files = ['cci.bib', 'oc_no_duplicates.bib', 'output.bib']
find_common_references(main_bib_file, folder_path)
