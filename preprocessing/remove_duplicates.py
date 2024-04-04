# Removes duplicate entries from BibTeX (.bib) files. It can process a single file or all files in a directory,
# identifying duplicates by their unique 'ID' or by comparing all fields. The output is saved to a specified location, 
# either as a modified single file or within a new directory for multiple files, with statistics on duplicates printed to the console.

import os
import glob
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def remove_duplicates_from_bib_file(input_file, output_file):
    with open(input_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        initial_count = len(bib_database.entries)
        unique_entries = {}
        for entry in bib_database.entries:
            unique_entries[entry['ID']] = entry  # Assumes 'ID' is unique for each entry
        
        final_count = len(unique_entries)
        duplicates_count = initial_count - final_count

        bib_database.entries = list(unique_entries.values())
        writer = BibTexWriter()
        with open(output_file, 'w', encoding='utf-8') as bibtex_out:
            bibtex_out.write(writer.write(bib_database))
        
        return initial_count, duplicates_count, final_count
    
def remove_complete_duplicates(bib_file_path, output_file_path):
    with open(bib_file_path, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
        initial_count = len(bib_database.entries)
        unique_entries = []

        for entry in bib_database.entries:
            if entry not in unique_entries:
                unique_entries.append(entry)

        duplicates_count = initial_count - len(unique_entries)

        # Create a new BibDatabase instance for the unique entries
        unique_bib_database = BibDatabase()
        unique_bib_database.entries = unique_entries

        # Write the unique entries to the output file
        writer = BibTexWriter()
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            out_file.write(writer.write(unique_bib_database))
    
    print(f'Initial number of references: {initial_count}')
    print(f'Number of duplicates: {duplicates_count}')
    print(f'Final number of references: {len(unique_entries)}')

def process_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    bib_files = glob.glob(f"{input_folder}/*.bib")
    total_files = len(bib_files)

    for i, input_file in enumerate(bib_files, start=1):
        filename = os.path.basename(input_file)
        output_file = os.path.join(output_folder, filename)
        print(f'Processing file {i}/{total_files}: {filename}')
        
        initial_count, duplicates_count, final_count = remove_duplicates_from_bib_file(input_file, output_file)
        print(f'Initial number of references: {initial_count}')
        print(f'Number of duplicates: {duplicates_count}')
        print(f'Final number of references: {final_count}')
        print('-'*30)

# Example usage:

# Choose from 'file', 'file_complete', 'folder'
# If 'file', duplicate entries are entries with common ID
# If 'file_complete', duplicate are entries with every field identical
task = 'file_complete'
# Update this with the path to your .bib file or folder containing .bib files                       
input = './data/cci/cci_papers_merged.bib'
# Update this with the path to the file or folder where you want to save the new .bib files
output = input[:-4] + '_no_duplicates.bib'

if task == 'file':
    remove_duplicates_from_bib_file(input, output)
elif task == 'file_complete':
    remove_complete_duplicates(input, output)
elif task == 'folder':
    process_folder(input, output)
