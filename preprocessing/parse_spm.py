"""Reads a specified text file, parses sections delineated by exact format rules
(capital letter followed by numbers and periods), consolidates content into a single continuous string,
and extracts cleaned reference lists, then stores and prints this data using a custom `SPM` class."""

import re

class SPM:
    def __init__(self, section, content, references):
        self.section = section
        self.content = content
        self.references = [ref.strip() for ref in references.split(',') if ref.strip()]

def parse_sections(filename):
    # Read the entire file
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Normalize line breaks
    content = content.replace('\r\n', '\n')

    # Split content by double newlines to isolate sections
    raw_sections = re.split(r'\n\n', content)

    # Prepare to collect SPM objects
    sections = []

    # Define regex for parsing individual sections
    pattern = r'^\s*([A-Z](?:\.\d{1,2})*)\s(.*?)\s*\{(.*)\}.*$'

    # Process each potential section
    for raw_section in raw_sections:
        match = re.match(pattern, raw_section, re.DOTALL)
        if match:
            section_number, section_content, section_references = match.groups()
            # Remove new lines and extra spaces from content
            cleaned_content = re.sub(r'\s+', ' ', section_content).strip()
            # Create an SPM object with cleaned data
            sections.append(SPM(section_number, cleaned_content, section_references.strip()))

    return sections

# Specify the path to your text file
filename = './data/cci/wg1_spm.txt'
sections = parse_sections(filename)

# Example to print out the parsed data
for section in sections:
    print(f'Section: {section.section}')
    print(f'Content: {section.content}')
    print(f'References: {section.references}')
    print('---'*20)
