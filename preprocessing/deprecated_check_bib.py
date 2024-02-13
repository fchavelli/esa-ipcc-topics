import bibtexparser
import openpyxl
import re

def preprocess_text(text):
    """
    Preprocesses text by removing special characters, converting to lowercase, and stripping whitespace.
    
    Parameters:
    - text: The text to preprocess.
    
    Returns:
    - The preprocessed text.
    """
    text = text or ""  # Ensure text is not None
    return re.sub(r'\W+', ' ', text).lower().strip()

def check_titles_in_excel(bib_file_path, excel_file_path):
    """
    Reads titles from a BibTeX file and checks if each can be found in column B of an Excel file.
    
    Parameters:
    - bib_file_path: Path to the BibTeX file.
    - excel_file_path: Path to the Excel file.
    
    Returns:
    - total_entries: The total number of entries in the BibTeX file.
    - no_match_count: The number of entries with titles not found in the Excel file.
    """
    with open(bib_file_path, encoding='utf-8') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    total_entries = len(bib_database.entries)
    
    # Load the Excel file
    wb = openpyxl.load_workbook(excel_file_path)
    sheet = wb.active
    
    # Get all titles from column B
    excel_titles = [preprocess_text(cell.value) for cell in sheet['B'] if cell.row > 1]  # Skip header row
    
    no_match_count = 0
    for entry in bib_database.entries:
        bib_title = preprocess_text(entry.get('title', ''))
        if bib_title not in excel_titles:
            print(f"Title not found in Excel: {entry['title']}")
            no_match_count += 1
            
    return total_entries, no_match_count

# Example usage
bib_file_path = 'output.bib'  # Change to your BibTeX file path
excel_file_path = '../data/cci/cci_papers.xlsx'  # Change to your Excel file path
total_entries, no_match_count = check_titles_in_excel(bib_file_path, excel_file_path)
print(f"Total entries: {total_entries}, Entries with no match: {no_match_count}")