"""
Input: multisheet spreadsheet with one row per reference (identified by DOI) with section information
Output: multisheet spreadsheet with on row per section (truncated), with references information (identified by DOI)
Truncature is up to first subsection (e.g. 10.2.3.1 becomes 10.2)

Example:

DOI           Sections
10.xxx1       10.1.3;11.2.4
10.xxx2       11.2.4

Section       DOI    
10.1          10.xxx1
11.2          10.xxx1; 10.xxx2
"""

import pandas as pd

# Reads an Excel file, processes sheets with 'Sections', truncates section names, pairs with DOIs, and sorts sections before saving to an Excel file
def process_excel_sheets(filename, output_filename):
    # Load the Excel file
    xl = pd.ExcelFile(filename)
    
    # Initialize a dictionary to store results from all sheets
    results = {}

    # Process each sheet
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        # Check if both 'Sections' and 'DOI' columns are present
        if 'Sections' in df.columns and 'DOI' in df.columns:
            # Initialize a dictionary for this sheet
            section_doi_dict = {}
            # Iterate through each row
            for _, row in df.iterrows():
                # Split sections by ";" and preprocess them
                sections = str(row['Sections']).split(';')
                for section in sections:
                    # Truncate the section to keep only before the second "."
                    truncated_section = '.'.join(section.split('.')[:2])
                    # Store or append the DOI in the dictionary
                    if truncated_section not in section_doi_dict:
                        section_doi_dict[truncated_section] = set()
                    section_doi_dict[truncated_section].add(row['DOI'])
                    
            # Store the dictionary for this sheet in the results
            results[sheet_name] = section_doi_dict

    # Write the results to a new Excel file
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        for sheet_name, data in results.items():
            # Convert the dictionary to a DataFrame for writing to Excel
            # Create lists for sections and their corresponding DOI lists
            # Sort the sections before creating DataFrame
            sorted_sections = sorted(data.keys())
            sections = []
            dois = []
            for section in sorted_sections:
                sections.append(section)
                dois.append('; '.join(data[section]))  # Join multiple DOIs with a semicolon
            # Create DataFrame
            df_to_save = pd.DataFrame({
                'Section': sections,
                'DOIs': dois
            })
            # Write DataFrame to a sheet in the Excel workbook
            df_to_save.to_excel(writer, sheet_name=sheet_name, index=False)

# Specify the path to your Excel file and the output file
input_filename = './data/cci/matched_references_unique_curated.xlsx'
output_filename = './data/cci/matched_sections.xlsx'
process_excel_sheets(input_filename, output_filename)