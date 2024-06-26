import re
import logging
import requests
import pandas as pd
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

# Specify the path to your Excel file
bib_file_path = './data/cci'
excel_file_path = './data/cci/cci_oc_papers.xlsx'
excel_name = excel_file_path.split('/')[-1][:-5]

# Specify the log level: 'INFO' or 'ERROR'
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',  # Do Not Track Request Header
    'Connection': 'keep-alive'
}

# Initialize counters
reference_from_doi_count = 0
reference_from_query_count = 0
error_count = 0

# Open error and warning log files
error_log_file = open(f'./logs/{excel_name}_error_log.txt', 'w', encoding='utf-8')
warning_log_file = open(f'./logs/{excel_name}_warning_log.txt', 'w', encoding='utf-8')

# Update the functions to write to the error and warning logs
def log_error(message):
    error_log_file.write(message + '\n')

def log_warning(message):
    warning_log_file.write(message + '\n')

def remove_non_alphanumeric_at_end(s):
    pattern = r'(full|fulltext\.html)$'
    cleaned_text = re.sub(pattern, '', s)
    return re.sub(r'[^\w\d]+$', '', cleaned_text)

# Function to find DOI or URL in text and display the process
def find_doi_or_url(text):
    doi_regex = r'(?:^|\b)10\.(\d{4,9}/[-._;()/:A-Za-z0-9]+)'
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    doi_match = re.search(doi_regex, text)
    if doi_match:
        logging.info("DOI found in reference content.")
        return ('doi', remove_non_alphanumeric_at_end(doi_match.group(0)))
    url_match = re.search(url_regex, text)
    if url_match:
        logging.info("URL found in reference content, will attempt to extract DOI from the webpage.")
        return ('url', remove_non_alphanumeric_at_end(url_match.group(0)))
    logging.info("No DOI or URL found in reference content, proceeding with query.")
    return ('query', text)

# Function to attempt fetching a DOI from webpage content and display the process
def extract_doi_from_webpage(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        doi_match = re.search(r'10.\d{4,9}/[-._;()/:A-Za-z0-9]+', response.text)
        if doi_match:
            logging.info("DOI successfully extracted from webpage content.")
            return remove_non_alphanumeric_at_end(doi_match.group(0))
        else:
            logging.info("No DOI found in webpage content.")
    except requests.RequestException as e:
        logging.error(f'Error accessing URL {url}: {e}')
    return None

def fetch_crossref_data(mode, content, reference_id):
    global doi_in_content_count, doi_from_url_count, reference_from_query_count
    if mode == 'doi':
        url = f'https://api.crossref.org/works/{content}'
    elif mode == 'query':
        url = f'https://api.crossref.org/works?query={content}&select=title,DOI,published,author,container-title,volume,page,issue,type&rows=1'
        log_warning(f'Reference ID {reference_id}: Entry recovered using query : {content}')
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['message'] if mode != 'query' else data['message']['items'][0]
    except requests.RequestException as e:
        log_error(f'Reference ID {reference_id}: Error fetching data for {content}: {str(e)}')
        return None

def process_bibtex_entry(item, project_field):
    # Simplified version, expand based on actual BibTeX requirements
    entry = {
        'ENTRYTYPE': 'article',  # Default type, adjust as needed
        'ID': item.get('DOI', '').replace('/', '_'),
        'title': item.get('title', ['No Title'])[0] if item.get('title') else 'No Title',
        'author': ' and '.join([f"{author.get('given', '')} {author.get('family', '')}" for author in item.get('author', [])]),
        'journal': item.get('container-title', ['No Journal'])[0] if item.get('container-title') else 'No Journal',
        'year': str(item.get('published', {}).get('date-parts', [[None]])[0][0]) if item.get('published', {}) else 'No Year',
        'volume': item.get('volume', 'No Volume'),
        'number': item.get('issue', 'No Issue'),
        'pages': item.get('page', 'No Pages'),
        'doi': item.get('DOI', 'No DOI'),
    }
    if project_field:
        entry['project'] = process_project_name(str(project_field).title().rstrip()) # Custom field for project
    return entry

def process_project_name(project):
    if project == 'Ghg':
        return 'Greenhouse Gases'
    elif project in ['Reccap-2', 'Cmug', 'Ar5']:
        return project.upper()
    else:
        return project

# Initialize the BibTeX database
db = BibDatabase()

# Load the Excel file into a DataFrame
df = pd.read_excel(excel_file_path)
total_references = len(df)

# Check for 'Project' field
project = (df.shape[1] == 2)
if project == False:
    project_field = None

# Process each reference in the DataFrame
for index, row in df.iterrows():
    reference_id = index + 1
    if project:
        project_field = row.iloc[0]  # Assuming project field is in the first column
        reference_content = row.iloc[1]  # Assuming reference content is in the second column
    else:
        reference_content = row.iloc[0] # Assuming reference content is in the first column
    logging.info(f'Reference {reference_id}/{total_references}')

    mode, content = find_doi_or_url(reference_content)
    if mode == 'url':
        extracted_doi = extract_doi_from_webpage(content)
        if extracted_doi:
            mode, content = ('doi', extracted_doi)
            logging.info(f'Reference ID {reference_id}: DOI extracted from URL.')
        else:
            mode, content = ('query', reference_content)
            logging.warning(f'Reference ID {reference_id}: No DOI found, using query mode.')

    item = fetch_crossref_data(mode, content, reference_id)
    if item:
        bibtex_entry = process_bibtex_entry(item, project_field)
        db.entries.append(bibtex_entry)
        logging.info(f'Successfully processed Reference ID {reference_id} using {mode}.')
        if mode == 'doi':
            reference_from_doi_count += 1
        elif mode == 'query':
            reference_from_query_count += 1
    else:
        logging.error(f'Failed to process Reference ID {reference_id}.')
        error_count += 1
        continue  # Skip to the next reference if unable to process

# Write the BibTeX entries to a file
with open(f'{bib_file_path}/{excel_name}.bib', 'w', encoding='utf-8') as bibtex_file:
    bibtex_writer = BibTexWriter()
    bibtex_file.write(bibtex_writer.write(db))

print(f"Finished processing all {total_references} references. Check '{excel_name}.bib' for the BibTeX entries. Check 'error_log.txt' for errors and 'warning_log.txt' for general logs.")

# After processing all references, print the summary and close log files
print(f"Summary:\n- References processed with DOI in content or extracted from webpage: {reference_from_doi_count}\n- References processed from query: {reference_from_query_count}\n- References failing to process: {error_count}")

# Close the log files
error_log_file.close()
warning_log_file.close()