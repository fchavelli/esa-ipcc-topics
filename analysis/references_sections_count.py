import pandas as pd

input_file = './data/cci/matched_references_unique_curated.xlsx'
output_file = './results/matched_references_sections_count.xlsx'
sheet_name = 'wg1'

# Load the Excel file
xls = pd.ExcelFile(input_file)  # replace with your file path

# Read the 'wg1' sheet into a DataFrame
df_wg1 = pd.read_excel(xls, sheet_name)

# Create a new DataFrame for the output
df_output = pd.DataFrame(columns=['Sections', 'Count of CCI Publications'])

# Split the 'Sections' column into individual sections and count them
sections_dict = {}
for sections in df_wg1['Sections']:
    temp_list = []
    for section in sections.split(';'):
        # Truncate the section, removing everything before the second dot
        truncated_section = '.'.join(section.split('.')[:2]).strip()
        if truncated_section in sections_dict:
            if truncated_section not in temp_list:
                temp_list.append(truncated_section)
                sections_dict[truncated_section] += 1
        else:
            sections_dict[truncated_section] = 1
            temp_list.append(truncated_section)

# Add the sections and their counts to the output DataFrame
for section, count in sections_dict.items():
    df_output = df_output._append({'Sections': section, 'Count of CCI Publications': count}, ignore_index=True)

# Write the output DataFrame to a new Excel file
df_output.to_excel(output_file, index=False)