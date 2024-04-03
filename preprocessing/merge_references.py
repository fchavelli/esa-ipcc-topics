import bibtexparser
from bibtexparser.bwriter import BibTexWriter

def load_bibtex_file(filepath):
    with open(filepath, encoding='utf-8') as bibtex_file:
        return bibtexparser.load(bibtex_file)

def save_bibtex_file(database, filepath):
    writer = BibTexWriter()
    with open(filepath, 'w', encoding='utf-8') as bibtex_file:
        bibtex_file.write(writer.write(database))

# Load the BibTeX databases
website_db = load_bibtex_file('./data/cci/cci_papers_website_complete.bib')
new_entries_db = load_bibtex_file('./data/cci/cci_papers_no_duplicates.bib')

# Prepare counters
added_new_entries_count = 0
added_updated_entries_count = 0

# Mapping of DOIs to IDs for existing entries
existing_dois = {entry['doi']: entry for entry in website_db.entries if 'doi' in entry}

for entry in new_entries_db.entries:
    if 'doi' in entry:
        doi = entry['doi']
        project = entry.get('project', None)
        # Check if the DOI is new or if the project is different and not empty
        if doi not in existing_dois:
            website_db.entries.append(entry)
            added_new_entries_count += 1
        else:
            existing_entry = existing_dois[doi]
            # Add the entry if the project field is different, not empty, or not present
            if (project != existing_entry.get('project') and project) or ('project' not in existing_entry):
                # Modify entry ID to include project name if it's specified
                if project:
                    entry['ID'] = f"{entry['ID']}_{project.replace(' ', '_')}"
                website_db.entries.append(entry)
                added_updated_entries_count += 1

# Save the updated database
save_bibtex_file(website_db, './data/cci/cci_papers_merged.bib')

print(f"New entries added: {added_new_entries_count}")
print(f"Entries with updated IDs added: {added_updated_entries_count}")
