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

def write_dois_to_txt(dois, file_path, total_file_path=False):
    with open(file_path, 'w', encoding='utf-8') as txt_file:
        for doi in dois:
            txt_file.write(doi + '\n')
    if total_file_path:
        with open(total_file_path, 'a', encoding='utf-8') as txt_file:
            for doi in dois:
                txt_file.write(doi + '\n')

report_tags = ['sr15', 'srccl', 'srocc', 'wg1', 'wg2', 'wg3']

folder_path = './data/references_no_duplicates' # Update this with the path to your folder
total_file_path = f'./results/dois/ar6_dois_full.txt'

n_dois = 0
for tag in report_tags:
    txt_file_path = f'./results/dois/ar6_dois_{tag}.txt'
    dois = parse_bib_files(folder_path, tag)
    n_dois += len(dois)
    write_dois_to_txt(dois, txt_file_path, total_file_path)
    print(f'Total number of DOIs in {tag}: {len(dois)}')

if total_file_path:
    print(f'Total number of DOIs in ar6: {n_dois}')