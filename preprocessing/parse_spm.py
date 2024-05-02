import pandas as pd
import re

def clean_text(text):
    # Remove non-printable characters and control characters except newline
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

def parse_sections(filename):
    # Read the entire file
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Normalize line breaks
    content = content.replace('\r\n', '\n')

    # Split content by double newlines to isolate sections
    raw_sections = re.split(r'\n\n', content)

    # Prepare to collect section data in a list of dictionaries
    sections = []

    # Define regex for parsing individual sections
    #pattern = r'^\s*((?:[A-Z](?:\.\d{1,2})*)|Figure SPM\.\d{1,2}|Table SPM\.\d{1,2}|Box SPM\.\d{1,2})\s(.*?)\s*\{(.*)\}.*$'
    pattern = r'^\s*((?:[A-Z](?:\.\d{1,2})*)|Figure SPM\.\d{1,2}|Table SPM\.\d{1,2}|Box SPM(?:\.\d{1,2})+?)\s(.*?)\s*\{(.*)\}.*$'

    # Process each potential section
    for raw_section in raw_sections:
        match = re.match(pattern, raw_section, re.DOTALL)
        if match:
            section_number, section_content, section_references = match.groups()
            # Clean and remove new lines and extra spaces from content
            cleaned_content = clean_text(section_content)
            cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()
            # Prepare the references as a list of cleaned strings
            cleaned_references = '; '.join([clean_text(ref).strip() for ref in section_references.split(',') if clean_text(ref).strip()])
            # Append a dictionary to the sections list
            sections.append({
                'SPM section': section_number,
                'Content': cleaned_content,
                'Report sections': cleaned_references
            })

    return sections

def save_to_excel(data, output_file):
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    # Write the DataFrame to an Excel file
    df.to_excel(output_file, sheet_name='wg1', index=False)

# Specify the path to your text file
filename = './data/cci/wg1_spm.txt'
sections = parse_sections(filename)

# Specify the output Excel file path
output_excel_file = './data/cci/wg1_spm_sections.xlsx'

# Save the sections data as Excel
save_to_excel(sections, output_excel_file)

print(f"Data has been saved to {output_excel_file}")