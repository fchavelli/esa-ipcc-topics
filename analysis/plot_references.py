import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import matplotlib.pyplot as plt
from collections import Counter
import os

def parse_bib_file(file_path):
    """Parse the BibTeX file and return the database object."""
    with open(file_path, encoding='utf-8') as bibtex_file:
        parser = BibTexParser(common_strings=True)
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
    return bib_database

def count_projects(bib_database):
    """Count occurrences of each project value in the BibTeX entries."""
    project_counts = Counter()
    for entry in bib_database.entries:
        # Check if 'project' field exists and count its occurrences
        if 'project' in entry and entry['project'] != '':
            project_counts[entry['project']] += 1
    return project_counts

def plot_project_counts(project_counts):
    """Plot and save a bar plot of the count of each project."""
    projects = list(project_counts.keys())
    counts = list(project_counts.values())
    
    plt.figure(figsize=(10, 8))
    plt.bar(projects, counts, color='skyblue')
    plt.xlabel('Project')
    plt.ylabel('Count')
    plt.title('Count of Each Project in BibTeX Entries')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
    
    # Ensure the directory exists
    output_dir = './plots/matched_projects'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the plot as a PDF
    plt.savefig(f'{output_dir}/project_counts.pdf')
    print(f'Plot saved as {output_dir}/project_counts.pdf')

# Example usage
file_path = './results/matched_references.bib'  # Replace with the path to your BibTeX file
bib_database = parse_bib_file(file_path)
project_counts = count_projects(bib_database)
plot_project_counts(project_counts)
