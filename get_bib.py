# This script reads an Excel file containing project references, queries the CrossRef API for each reference,
# and generates a BibTeX file with entries for each reference including additional information such as
# authors, journal, volume, pages, and number when available. It also maps various document types from CrossRef
# to corresponding BibTeX entry types.

# Import necessary libraries:
# pandas for reading Excel files,
# requests for making HTTP requests to the CrossRef API,
# urllib.parse.quote for URL encoding of references,
# bibtexparser for creating and writing BibTeX entries,
# and BibTexWriter from bibtexparser for formatting the BibTeX file.

# Define a mapping from CrossRef document types to BibTeX entry types.
# This mapping is used to translate the document type provided by CrossRef
# to the corresponding BibTeX entry type. The script includes a basic mapping
# and can be extended to cover more types as needed.

# Load the Excel file specified by the user.
# The Excel file should have at least two columns: "Project" and "Reference".
# The path to this file must be updated by the user.

import pandas as pd
import requests
from urllib.parse import quote
import bibtexparser
from bibtexparser.bwriter import BibTexWriter

# Load the Excel file
excel_file = 'data/cci_papers.xlsx'  # Update this to the path of your Excel file
df = pd.read_excel(excel_file)

# Initialize a BibTeX writer
writer = BibTexWriter()

# Initialize an empty list to store BibTeX entries
bibtex_entries = []

# Start processing
print("Starting to process references...")

# Counter for processed references
processed_count = 0
total_references = len(df)

for index, row in df.iterrows():
    print(f"Processing reference {processed_count+1}/{total_references}")
    
    # Encode the reference for URL
    encoded_reference = quote(row['Reference'])
    
    # Construct the request URL
    url = f"https://api.crossref.org/works?query.title={encoded_reference}&select=title,DOI,published,author,container-title,volume,page,issue,type&rows=1"
    
    try:
        # Make the request
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if there are items in the response
            if data['message']['items']:
                item = data['message']['items'][0]
                
                # Format authors if available
                authors = item.get('author', [])
                author_names = []

                for author in authors:
                    # Build the name string based on available fields
                    if 'given' in author and 'family' in author:
                        author_name = f"{author['given']} {author['family']}"
                    elif 'family' in author:
                        author_name = author['family']
                    elif 'name' in author:
                        author_name = author['name']
                    else:
                        author_name = "Unknown"

                    # Append the constructed name to the author_names list
                    author_names.append(author_name)

                # Join all author names with ' and ' as required for BibTeX format
                author_names = ' and '.join(author_names)
                
                # Determine the BibTeX entry type
                crossref_type = item.get('type', '')
                entry_type = 'article'  # Default entry type, adjust logic here for different types
                
                # Construct a BibTeX entry
                bibtex_entry = {
                    'ENTRYTYPE': entry_type,
                    'ID': item.get('DOI', '').replace('/', '_'),
                    'title': item.get('title', [])[0] if item.get('title') else '',
                    'doi': item.get('DOI', ''),
                    'year': str(item.get('published', {}).get('date-parts', [[None]])[0][0]) if item.get('published', {}).get('date-parts') else '',
                    'author': author_names,
                    'journal': item.get('container-title', [])[0] if item.get('container-title') else '',
                    'volume': item.get('volume', ''),
                    'pages': item.get('page', ''),
                    'number': item.get('issue', ''),
                    'project': str(row['Project']).rstrip()
                }
                
                # Append the entry to the list
                bibtex_entries.append(bibtex_entry)
                
                print(f"Successfully processed reference.")
            else:
                print(f"No items found for reference '{row['Reference']}'. Skipping...")
        else:
            print(f"Error fetching data for reference '{row['Reference']}' (HTTP status {response.status_code}). Skipping...")

    except requests.exceptions.RequestException as e:
        print(f"Request error for reference '{row['Reference']}': {e}. Skipping...")
    except ValueError as e:
        print(f"Error decoding JSON response for reference '{row['Reference']}': {e}. Skipping...")
    
    processed_count += 1

# Add entries to a database
db = bibtexparser.bibdatabase.BibDatabase()
db.entries = bibtex_entries

# Write the BibTeX file
with open('output.bib', 'w', encoding='utf-8') as bibtex_file:
    bibtex_file.write(writer.write(db))

print("Finished processing all references. Check the output.bib file for results.")
