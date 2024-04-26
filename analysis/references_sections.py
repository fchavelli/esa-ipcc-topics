import pandas as pd
import os
import re

def read_excel(path):
    """ Load the Excel workbook with multiple sheets. """
    return pd.ExcelFile(path)

def find_citations(text, regex, doi, chapter):
    """ Search for reference citations in the text using a specific regex pattern. """
    found_citations = []
    current_section = None
    section_name = None
    section_regex = r'^(' + chapter + r'(\.\d+)*)\s+(.*)$'

    for line in text.split('\n'):
        section_match = re.match(section_regex, line)
        if section_match:
            current_section = section_match.group(1)
            section_name = section_match.group(3)
        
        if re.search(regex, line):
            if current_section != None:
                if len(current_section) > 1:
                    print(current_section,section_name,line)
                    found_citations.append({
                        'DOI': doi,
                        'Section': current_section,
                        'SectionName': section_name,
                        'Context': line
                    })
    
    return found_citations

def process_reports(excel_path, text_directory, output_path):
    xls = read_excel(excel_path)
    writer = pd.ExcelWriter(output_path)

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        all_citations = []

        for _, row in df.iterrows():
            reference = row['First Author'] + r'.*\b' + str(row['Year']) + r'\b'
            chapters = str(row['Chapters']).split(';')
            chapter_files = [f for f in os.listdir(text_directory) 
                             if any(f'ch{ch.strip()}' in f for ch in chapters)]

            for file_name in chapter_files:
                chapter = re.search(r"_ch(\d+)", file_name).group(1)
                file_path = os.path.join(text_directory, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    citations = find_citations(text, reference, row['DOI'], chapter)
                    all_citations.extend(citations)

        # Aggregating and merging citations into DataFrame
        if all_citations:
            citations_df = pd.DataFrame(all_citations)
            aggregated_data = citations_df.groupby('DOI').agg({
                'Section': lambda x: '; '.join(set(x.dropna())),
                'SectionName': lambda x: '; '.join(set(x.dropna())),
                'Context': lambda x: ' | '.join(set(x.dropna()))
            }).reset_index()

            df = pd.merge(df, aggregated_data, on='DOI', how='left')
        
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer._save()

excel_path = './data/cci/matched_references_unique_formated.xlsx'
text_directory = './data/reports/txt'
output_path = './results/matched_references_sections.xlsx'
process_reports(excel_path, text_directory, output_path)

