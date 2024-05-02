import pandas as pd

def process_excel_files(spm_path, matched_path, output_path):
    """Processes two Excel files to match sections and append DOI references.
    
    The `wg1_spm_sections.xlsx` contains sections with content and report sections, while
    `matched_sections.xlsx` contains mappings from sections to DOIs. This script reads each sheet
    from `wg1_spm_sections`, matches DOIs based on report sections, and appends a new column
    with these DOIs in a new file `cci_references_spm_sections.xlsx`.
    """
    # Try to load the wg1_spm_sections workbook
    try:
        spm_sheets = pd.read_excel(spm_path, sheet_name=None)
    except Exception as e:
        print(f"Failed to read {spm_path}: {e}")
        return
    
    # Try to load the matched_sections workbook
    try:
        matched_sheets = pd.read_excel(matched_path, sheet_name=None)
    except Exception as e:
        print(f"Failed to read {matched_path}: {e}")
        return

    # Writer to save to new workbook
    writer = pd.ExcelWriter(output_path)

    # Process each sheet in wg1_spm_sections
    for sheet_name, spm_df in spm_sheets.items():
        print(f"Processing sheet: {sheet_name}")
        
        if sheet_name in matched_sheets:
            matched_df = matched_sheets[sheet_name]
            # Create a dictionary for fast lookup of DOIs by Section
            doi_dict = {str(row['Section']).strip(): row['DOIs'] for index, row in matched_df.iterrows()}

            # Function to find DOIs based on Report sections
            def find_dois(report_sections):
                doi_list = []
                sections = str(report_sections).split('; ')
                for section in sections:
                    section = section.strip()  # Strip whitespace for matching
                    if section in doi_dict:
                        doi_list.append(doi_dict[section])
                return ";".join(doi_list)

            # Apply function to create CCI references column
            spm_df['CCI references'] = spm_df['Report sections'].apply(find_dois)
        else:
            print(f"No matching sheet found in matched_sections for {sheet_name}, skipping DOI matching.")
            spm_df['CCI references'] = ""

        # Save processed dataframe to new sheet in the output workbook
        spm_df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Save and close the writer
    writer._save()
    writer.close()
    print(f"Processed data saved to {output_path}")

# Define file paths
spm_path = './data/cci/wg1_spm_sections.xlsx'
matched_path = './data/cci/matched_sections.xlsx'
output_path = './results/cci_references_spm_sections.xlsx'

# Call the function with the paths
process_excel_files(spm_path, matched_path, output_path)
