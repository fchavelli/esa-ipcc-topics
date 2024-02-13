# This Python script is designed to automate the extraction and formatting of bibliographic references from an Excel spreadsheet into BibTeX format, specifically for academic papers.
# It involves several key steps and utilizes various libraries to handle data extraction, web requests, and text processing. Here's an overview of its functionality and components:

# ### Dependencies:
# - **pandas**: For reading data from an Excel file.
# - **requests**: For making HTTP requests to fetch web pages or API data.
# - **re (Regular Expressions)**: For pattern matching in strings, particularly to identify DOIs and URLs.
# - **urllib.parse**: Specifically, `quote` is used for URL encoding.
# - **bibtexparser**: For creating and writing BibTeX entries.

# ### Main Steps:

# 1. **Loading Data**: The script starts by loading an Excel file containing references into a pandas DataFrame. The file path is specified in `excel_file`.

# 2. **Initialization**:
#    - A BibTeX writer (`BibTexWriter`) is initialized to format the output correctly.
#    - Two log files are defined: `error_file` for errors and `warning_file` for warnings, to log issues encountered during processing.

# 3. **Processing References**: The script iterates over each row in the DataFrame, performing the following tasks:
#    - It attempts to find a DOI within the reference string. If a DOI is not directly found, it makes a web request to a URL (if present) to try and extract a DOI from the webpage content.
#    - If a DOI is found, it fetches the paper's metadata from the CrossRef API using the DOI.
#    - If no DOI is found, it queries the CrossRef API with the reference title to attempt to find a matching entry and retrieve its metadata.
#    - It then formats the fetched metadata into a BibTeX entry using the `process_bibtex_entry` function and appends this entry to a list of BibTeX entries.

# 4. **Error and Warning Logging**:
#    - Errors (e.g., issues fetching webpage content, API request errors) are logged to `error_log.txt`.
#    - Warnings (e.g., references for which DOIs had to be recovered through a title search) are logged to `warning_log.txt`.

# 5. **Creating BibTeX File**: After processing all references, the script compiles the BibTeX entries into a database and writes this database to a `.bib` file.

# 6. **Final Output**: The script prints a summary of the processing, including the number of references processed with direct DOIs, those for which DOIs were recovered, and counts of fetching and other errors encountered.

# ### Functions:
# - `process_bibtex_entry(item, row, entries_list)`: Formats and appends a BibTeX entry to the list of entries.
# - `remove_non_alphanumeric_at_end(s)`: Cleans the DOI string by removing any non-alphanumeric character at the end.
# - `find_doi_in_string(s, item_id)`: Attempts to find a DOI in a given string or through a URL contained in the string.
# - `log_error(message, file_name)` and `log_warning(message, file_name)`: Log error and warning messages to their respective files.


import pandas as pd
import requests
import re
import bibtexparser
from bibtexparser.bwriter import BibTexWriter

# Load the Excel file
excel_file = 'data/cci/cci_papers_toy.xlsx'  # Update this to the path of your Excel file
error_file = 'error_log.txt'
warning_file ='warning_log.txt'

df = pd.read_excel(excel_file)

# Initialize a BibTeX writer
writer = BibTexWriter()

# Initialize an empty list to store BibTeX entries
bibtex_entries = []

# Start processing
print("Starting to process references...")

# Function to process and create a BibTeX entry
def process_bibtex_entry(item, row, entries_list):
    # Extract and format author names
    authors = item.get('author', [])
    author_names = []
    for author in authors:
        if 'given' in author and 'family' in author:
            author_name = f"{author['given']} {author['family']}"
        elif 'family' in author:
            author_name = author['family']
        elif 'name' in author:
            author_name = author['name']
        else:
            author_name = "Unknown"
        author_names.append(author_name)
    author_names_str = ' and '.join(author_names)

    # Determine the BibTeX entry type based on the CrossRef type, with a default of 'article'
    crossref_type_to_bibtex_type = {
        'journal-article': 'article',
        # Add more mappings as needed
    }
    entry_type = crossref_type_to_bibtex_type.get(item.get('type'), 'misc')

    # Construct the BibTeX entry dictionary
    bibtex_entry = {
        'ENTRYTYPE': entry_type,
        'ID': item.get('DOI', '').replace('/', '_'),
        'title': item.get('title', [])[0] if item.get('title') else 'No Title',
        'author': author_names_str,
        'journal': item.get('container-title', [])[0] if item.get('container-title') else '',
        'year': str(item.get('published', {}).get('date-parts', [[None]])[0][0]) if item.get('published', {}).get('date-parts') else '',
        'volume': item.get('volume', ''),
        'number': item.get('issue', ''),
        'pages': item.get('page', ''),
        'doi': item.get('DOI', ''),
        'project': str(row['Project']).rstrip()
    }

    # Append the constructed entry to the list
    entries_list.append(bibtex_entry)

def remove_non_alphanumeric_at_end(s):
    # Regex explanation:
    # [^\w\d]+$ - Matches one or more (+) non-word characters (\W) or non-digit characters at the end of the string ($)
    # \w includes letters, digits, and underscores; \d includes digits. The ^ inside the brackets negates the set.
    return re.sub(r'[^\w\d]+$', '', s)

# Function for finding DOI or making web requests
def find_doi_in_string(s, item_id):
    doi_regex = r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+'
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    doi_match = re.search(doi_regex, s)
    if doi_match:
        return remove_non_alphanumeric_at_end(doi_match.group(0))
    
    url_match = re.search(url_regex, s)
    if url_match:
        url = url_match.group(0)
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                webpage_content = response.text
                doi_match_webpage = re.search(doi_regex, webpage_content)
                if doi_match_webpage:
                    print('doi_url', doi_match.group(0))
                    return doi_match_webpage.group(0)
        except requests.RequestException as e:
            log_error(f"Item ID {item_id}: Error fetching the webpage: {e}", error_file)
    return None

# Function to log errors and warnings to a file
def log_error(message, file_name):
    with open(file_name, 'a', encoding='utf8') as f:
        f.write(message + "\n")
def log_warning(message, file_name):
    with open(file_name, 'a', encoding='utf8') as f:
        f.write(message + "\n")

doi_count = 0
url_count = 0
fetch_err_count = 0
other_err_count = 0

# Process references
for index, row in df.iterrows():
    print(f"Processing reference {index+1}/{len(df)}")
    
    encoded_reference = row['Reference']
    doi = find_doi_in_string(encoded_reference, index)
    if doi:
        url = f"https://api.crossref.org/works/{doi}"
        doi_count += 1
    else:
        url = f"https://api.crossref.org/works?query={encoded_reference}&select=title,DOI,published,author,container-title,volume,page,issue,type&rows=1"
        url_count += 1
        log_warning(f"Check reference {index}: '{row['Reference']}'", warning_file)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            item = data['message'] if doi else data['message']['items'][0] if data['message']['items'] else None
            if item:
                process_bibtex_entry(item, row, bibtex_entries)
            else:
                print(f"No items found for reference '{row['Reference']}'. Skipping...")
        else:
            log_error(f"Error fetching data for reference {index+1} '{row['Reference']}' (HTTP status {response.status_code})", error_file)
            print('Error fetching data')
            fetch_err_count += 1
    except requests.exceptions.RequestException as e:
        log_error(f"Request error for reference '{row['Reference']}': {e}", error_file)
        other_err_count += 1

# Write the BibTeX file
db = bibtexparser.bibdatabase.BibDatabase()
db.entries = bibtex_entries
with open('output.bib', 'w', encoding='utf-8') as bibtex_file:
    bibtex_file.write(writer.write(db))

print("Finished processing all references. Check the output.bib file for results.")
print(f'Processed {doi_count} references with DOI and {url_count} references with recovered DOI (check warning_log.txt for details).')
print(f'Encontered {fetch_err_count} fetching errors and {other_err_count} other errors (check error_log.txt for details).')
