import bibtexparser

def remove_duplicates_from_bib(input_file, output_file):
    """
    Reads a BibTeX file, removes duplicate entries, and writes the unique entries to a new file.
    
    Parameters:
    - input_file: Path to the input BibTeX file.
    - output_file: Path where the output BibTeX file with deduplicated entries will be written.
    
    Returns:
    - initial_count: The initial number of references in the input file.
    - duplicates_count: The number of duplicate references found.
    - new_count: The number of references in the new, deduplicated file.
    """
    with open(input_file, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    initial_count = len(bib_database.entries)
    # Convert each entry to a frozenset of its items to make them hashable and comparable
    unique_entries = set(frozenset(entry.items()) for entry in bib_database.entries)
    duplicates_count = initial_count - len(unique_entries)

    # Convert the unique entry sets back to dictionaries
    unique_entries_dicts = [dict(entry) for entry in unique_entries]
    
    # Update the database with unique entries
    bib_database.entries = unique_entries_dicts
    new_count = len(bib_database.entries)

    with open(output_file, 'w', encoding='utf-8') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)
    
    return initial_count, duplicates_count, new_count

# Example usage
input_file = 'data/references/output.bib'  # Change this to the path of your input BibTeX file
output_file = 'data/references/oc_no_duplicates.bib'  # Change this to where you want to save the output file
initial_count, duplicates_count, new_count = remove_duplicates_from_bib(input_file, output_file)
print(f"Initial references: {initial_count}, Duplicates removed: {duplicates_count}, New references count: {new_count}")
