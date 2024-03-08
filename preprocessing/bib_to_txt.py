import glob
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

def parse_bib_files(folder_path, filename_tag):
    bib_files = glob.glob(f"{folder_path}/*{filename_tag}*.bib")
    all_dois = []

    for bib_file in bib_files:
        with open(bib_file, 'r', encoding='utf-8') as bibtex_file:
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            bib_database = bibtexparser.load(bibtex_file, parser=parser)
            for entry in bib_database.entries:
                if 'doi' in entry:
                    all_dois.append(entry['doi'])

    return all_dois

def write_dois_to_txt(dois, file_path):
    with open(file_path, 'w', encoding='utf-8') as txt_file:
        for doi in dois:
            txt_file.write(doi + '\n')

folder_path = './data/references' # Update this with the path to your folder
filename_tag = 'sr15' # Update this with the tag to filter filenames
txt_file_path = 'sr15.txt'

dois = parse_bib_files(folder_path, filename_tag)
write_dois_to_txt(dois, txt_file_path)

print(f'Total number of DOIs: {len(dois)}')
