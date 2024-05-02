import pandas as pd
import os
import re

# Read data from an Excel workbook with multiple sheets
def read_excel(path):
    return pd.ExcelFile(path)

def create_chapter_regex(chapters):
    chapters_regex = '|'.join([re.escape(chapter.strip()) for chapter in chapters])
    print(r'^([' + chapters_regex + r'](\.\d+)*)\s+(.*)$')
    return r'^([' + chapters_regex + r'](\.\d+)*)\s+(.*)$'

# Read and process each text file to find citations
def find_citations(text, df, chapters):
    citations = {}
    current_section = None
    section_name = None
    chapter_regex = create_chapter_regex(chapters)

    for line in text.split('\n'):
        section_match = re.match(chapter_regex, line)

        if section_match:
            current_section = section_match.group(1)
            section_name = section_match.group(3)

        for _, row in df.iterrows():
            pattern = re.escape(row['First Author']) + r'.*\b' + str(row['Year']) + r'\b'
            if current_section != None:
                if re.search(pattern, line, re.IGNORECASE) and len(current_section) > 1:
                    print(current_section)
                    print(section_name)
                    print(row['First Author'])
                    print(line)
                    key = (row['DOI'])
                    if key not in citations:
                        citations[key] = {'Sections': [], 'Section Names': [], 'Contexts': []}
                    citations[key]['Sections'].append(current_section)
                    citations[key]['Section Names'].append(section_name)
                    citations[key]['Contexts'].append(line)
                
    # Update DataFrame with citations found
    for key, items in citations.items():
        matches = df['DOI'] == key
        df.loc[matches, 'Sections'] = '; '.join(items['Sections'])
        df.loc[matches, 'Section Names'] = '; '.join(items['Section Names'])
        df.loc[matches, 'Context'] = '| '.join(items['Contexts'])
    
    return df

# Process each report sheet and corresponding text files
def process_reports(excel_path, text_directory):
    xls = read_excel(excel_path)
    with pd.ExcelWriter('./results/matched_references_sections.xlsx') as writer:
        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            chapters = df['Chapters'].dropna().astype(str).str.split(';').explode().unique()
            chapter_filters = [f"ch{chapter.strip()}" for chapter in chapters]
            matching_files = [f for f in os.listdir(text_directory) if sheet_name in f and 'ch' in f and not 'sm' in f and any(ch_filter in f for ch_filter in chapter_filters)]
            print(f"Processing report: {sheet_name.upper()}")
            for file in matching_files:
                print(f"Processing file: {file}")
                with open(os.path.join(text_directory, file), 'r', encoding='utf-8') as f:
                    text = f.read()
                    df = find_citations(text, df, chapters)
            df.to_excel(writer, sheet_name=sheet_name, index=False)  # Save updated DataFrame to sheet

excel_path = './data/cci/matched_references_copy.xlsx'
text_directory = './data/reports/txt'
process_reports(excel_path, text_directory)