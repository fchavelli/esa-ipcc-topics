""" 
Input: Matching ESA CCI-IPCC references with unique references (several Projects and Chapters in the same row)
Output: Matching ESA CCI-IPCC references with one row per chapter (still several Projects in the same row)

Example:

Project             DOI                             Chapters
Soil Moisture	    10.1038/nature11377     ...     10;11

Project             DOI                             Chapter
Soil Moisture	    10.1038/nature11377     ...     10
Soil Moisture	    10.1038/nature11377	    ...     11
"""

import pandas as pd

def expand_chapters(data_frame):
    # This function will handle the expansion of the 'Chapters' column
    # Split the 'Chapters' column and explode it into multiple rows
    return (
        data_frame.drop('Chapters', axis=1)
        .join(
            # Split the 'Chapters' by ';' and expand into a list, then explode the list into rows
            data_frame['Chapters'].astype(str).str.split(';').explode()
        )
    )

def process_sheets(input_file_path, output_file_path):
    # Load the XLSX file with multiple sheets
    xls = pd.ExcelFile(input_file_path)

    # Create an Excel writer for the output file
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        # Iterate through each sheet in the Excel file
        for sheet_name in xls.sheet_names:
            # Read the current sheet
            df = pd.read_excel(xls, sheet_name=sheet_name)

            # Expand the 'Chapters' column into multiple rows
            expanded_df = expand_chapters(df)

            # Write the processed DataFrame back to a new sheet in the output Excel file
            expanded_df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("Processing complete. Output file saved as:", output_file_path)

# Example usage
input_path = './data/cci/matched_references_unique_formated.xlsx'
output_path = './results/matched_references_chapters_extended.xlsx'
process_sheets(input_path, output_path)
