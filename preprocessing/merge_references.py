import bibtexparser

# Load the BibTeX file where entries will be added (cci_papers_website.bib)
with open('./data/cci/cci_papers_website_copy.bib', encoding='utf8') as bibtex_file:
    bib_database_website = bibtexparser.load(bibtex_file)

# Convert entries to a dictionary for easier search by DOI
website_entries_by_doi = {entry.get('doi'): entry for entry in bib_database_website.entries}

# Load the BibTeX file with new entries (cci_papers.bib)
with open('./data/cci/cci_papers_no_duplicates.bib', encoding='utf8') as bibtex_file:
    bib_database_new = bibtexparser.load(bibtex_file)

# Prepare a list for entries to be added
entries_to_add = []

# Check each entry in the new database
for entry in bib_database_new.entries:
    doi = entry.get('doi')
    project = entry.get('project', '')
    
    # Check if DOI exists in the website database and if the project field is different when 'project' is {}
    if doi not in website_entries_by_doi or (website_entries_by_doi[doi].get('project', '') == '' and project != ''):
        entries_to_add.append(entry)
        print(entry.get('doi'))
        print(entry.get('title', ''))
        print(entry.get('project', ''))

# Add new entries to the website database
bib_database_website.entries.extend(entries_to_add)

# Write the updated database back to the file
with open('./data/cci/cci_papers_website_updated.bib', 'w', encoding='utf8') as bibtex_file:
    bibtexparser.dump(bib_database_website, bibtex_file)

print(f"Added {len(entries_to_add)} new entries to cci_papers_website.bib.")
