def clean_project_field(input_path, output_path):
    with open(input_path, 'r', encoding='utf8') as input_file:
        lines = input_file.readlines()
    
    with open(output_path, 'w', encoding='utf8') as output_file:
        for line in lines:
            if line.strip().startswith('project'):
                key, value = line.split('=', 1)
                # Remove surrounding spaces and braces, then convert to lowercase for case-insensitive comparison
                cleaned_value = value.strip().lower().rstrip()
                if 'ghg' in cleaned_value or 'reccap-2' in cleaned_value  or 'cmug' in cleaned_value or 'ar5' in cleaned_value or 'sst' in cleaned_value:
                    cleaned_value = cleaned_value.upper()
                elif 'nan' in cleaned_value:
                    cleaned_value = ''
                else:
                    cleaned_value = cleaned_value.title().rstrip()
                # Reconstruct the line with the possibly replaced value
                line = f"{key}= {cleaned_value}\n"
            output_file.write(line)

# Define the path to your input and output BibTeX files
input_file_path = 'data/references/cci_no_duplicates.bib'
output_file_path = 'data/references/cci_no_duplicates.bib'
clean_project_field(input_file_path, output_file_path)
