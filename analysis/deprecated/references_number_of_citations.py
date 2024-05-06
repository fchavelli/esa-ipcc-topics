import pandas as pd
import re

def count_citations(text, pattern):
    try:
        with open(text, 'r', encoding='utf-8') as file:
            content = file.read()
            matches = re.findall(pattern, content, re.DOTALL)  # Include re.DOTALL to handle line jumps
            print(matches)
            return len(matches)
    except FileNotFoundError:
        print(f"Warning: The file {text} was not found.")
        return 0

def process_excel(input_file, text_directory, output_file):
    # Load the Excel file
    xl = pd.ExcelFile(input_file)
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    
    # Process each sheet
    for sheet_name in xl.sheet_names:
        print(f"Processing sheet: {sheet_name}")
        df = xl.parse(sheet_name)
        
        # Add new columns to DataFrame
        df['Number of citations per chapter'] = ''
        df['Number of citations'] = 0
        
        # Iterate through each row to process citations
        for index, row in df.iterrows():
            citation_counts = []
            chapters = str(row['Chapters']).split(';')
            # Update the regex pattern to include optional spaces and/or a single newline character
            #pattern = re.escape(row['First Author']) + r'(?:\s|\n)*et(?:\s|\n)*al\.,(?:\s|\n)*' + str(row['Year'])
            pattern = re.escape(row['First Author']) + r'(?:\s|\n)*et(?:\s|\n)*al\.,(?:\s|\n)*'
            
            # Count occurrences for each chapter
            for chapter in chapters:
                filename = f"{text_directory}/{sheet_name}_ch{chapter}.txt"
                count = count_citations(filename, pattern)
                citation_counts.append(f"{chapter}:{count}")
                
            # Store the results in the DataFrame
            df.at[index, 'Number of citations per chapter'] = '; '.join(citation_counts)
            df.at[index, 'Number of citations'] = sum([int(x.split(':')[1]) for x in citation_counts])
        
        # Write processed DataFrame to the new Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Save the new Excel file
    writer._save()  # Corrected method call to save, not _save
    writer.close()
    print(f"Processing completed. Output file is saved in {output_file}.")

# Specify the input Excel file and other parameters
input_file = './data/cci/matched_references_unique_formated.xlsx'
text_directory = './data/reports/content'
output_file = './results/matched_references_number_of_citations.xlsx'
process_excel(input_file, text_directory, output_file)
