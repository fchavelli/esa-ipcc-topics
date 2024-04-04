import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from collections import defaultdict

def load_bibtex_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as bibtex_file:
        return bibtexparser.load(bibtex_file)

def save_bibtex_file(database, filepath):
    writer = BibTexWriter()
    with open(filepath, 'w', encoding='utf-8') as bibtex_file:
        bibtex_file.write(writer.write(database))

website_db = load_bibtex_file('./data/cci/intermediate/cci_papers_website_complete_no_duplicates.bib')
new_entries_db = load_bibtex_file('./data/cci/intermediate/cci_papers_no_duplicates.bib')

# Create a mapping of DOIs to list of projects and a set for IDs for quick lookup
doi_to_projects = defaultdict(set)
id_set = set(entry['ID'] for entry in website_db.entries)
for entry in website_db.entries:
    if 'doi' in entry and 'project' in entry:
        doi_to_projects[entry['doi']].add(entry['project'])

new_entries_added = 0
for entry in new_entries_db.entries:
    doi = entry.get('doi', '')
    project = entry.get('project', '')
    if doi not in doi_to_projects or (doi in doi_to_projects and project not in doi_to_projects[doi] and project != ''):
        # Check for unique ID before adding
        original_id = entry['ID']
        modified_id = f"{original_id}_{project.replace(' ', '_')}" if project else original_id
        if doi in doi_to_projects and project != '':
            while modified_id in id_set:
                modified_id += "_new"
            entry['ID'] = modified_id
        website_db.entries.append(entry)
        id_set.add(modified_id)
        new_entries_added += 1
        if doi in doi_to_projects:
            doi_to_projects[doi].add(project)

save_bibtex_file(website_db, './data/cci/cci_papers_merged.bib')
print(f"New entries added: {new_entries_added}")
