# ESA Climate Office - IPCC analysis
Analysis of ESA Climate Office topics across last IPCC reports

## Installation

Create a python virtual environment and install the dependencies.

shell

```shell
python -m venv env
.\env\Scripts\Activate
pip install -r requirements.txt
```

bash

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Data

# Data information and management

This folder is meant to store raw and processed IPCC and ESA data (reports, references...). It is organised as follows.

```
\data
    \cci                [cci references (.xlsx) and search terms (.json)]
    \reports
        \pdf            [ipcc report raw files (.pdf)]
        \txt            [ipcc report raw files (.txt)]
        \content        [ipcc report in-text content (.txt)]
        \references     [ipcc report in-text references (.txt)]
    \references         [esa & ipcc references (.bib)]
    \online_references  [ipcc references retrieved online (.xlsx)]
```

Download the available reports (.pdf) and references (.bib) from the IPCC website.
AR6 WG1,2,3 chapters and associated references can be downloaded automatically using the following command.

```
python download_reports.py
```

Other files including Special Reports (SR) and Synthesis Report (SYR) chapters, Summary for Policymakers (SPM), Technical Summaries (TS), Annexes (A) as well as references can be downloaded manually from the [IPCC website](https://www.ipcc.ch).

## Preprocessing

### IPCC Reports

#### Download PDF

Download the available reports (.pdf) and references (.bib) from the IPCC website.
AR6 WG1,2,3 chapters and associated references can be downloaded automatically using the following command.

```python
python download_reports.py
```

Other files including Special Reports (SR) and Synthesis Report (SYR) chapters, Summary for Policymakers (SPM), Technical Summaries (TS), Annexes (A) as well as references can be downloaded manually from the [IPCC website](https://www.ipcc.ch).

#### Convert PDF to TXT

Once pdf files are downloaded, they can be converted to txt files using the following command. The text in tables and figures are read when available (e.g. WG1 Chapter 1, Fig 1.1). Note that the process can take a few minutes.

```
python ./utils/pdf_to_txt.py
```

#### Split content and references

Report chapters in-text references have to be removed to not interfere in the counting process. The report txt files can be splitted into content and references using the following command. Note that manual check may be needed in case the chapter format is not as expected (content | references), typically for SRs. WGs chapters are processed correctly except for WG1 Chapter 1, WG3 Chapter 6 SM and WG3 Chapter 17 SM that don't have any reference section. Note that TS, SPM and SYR do not have in text references since they refer directly to report chapters.

```
python ./preprocessing/split_chapter_references.py
```

#### Parse SPMs

Use `parse_spm.py` code to parse SPM .txt files in a Excel spreadsheet with `Section`, `Content` and `References` columns as in the following example.
```
Section     Content                             References
A.1         It is unequivocal that human...     ['2.2', '2.3', ...]
```

### IPCC references

IPCC report references (.bib) can be downloaded from the IPCC website for all WGs chapters (but not for supplementary materials and annexes that are only available in text). Regarding SRs, it is possible to recover references from the `References` sections at the end of each report webpage. These raw, incomplete, duplicates references can be pasted in xlsx documents in `/data/online_references` and processed all at once (removing reference ids, empty rows and duplicates) using the following command.

```
python ./preprocessing/clean_online_references.py
```

Follow the procedure as for CCI references (described below) to create bib files from xlsx files. The expected Excel format is the following.
```
Reference
Nitta Tomoko (2017) Impact of Arctic Wetlands...
Famiglietti J S (2015) Satellites provide the...
...
```

### CCI references

Download the CCI references (.bib) or build a bibliography from an Excel file (containing at least a title or a doi for each reference). Reference metadata (including type, date, authors, journal, and doi) will be recovered online using Crossref API. The Excel file is expected to have the following structure with no empty rows.

```
Project         | Reference
Soil moisture   | Nitta Tomoko (2017) Impact of Arctic Wetlands...
Sea level       | Famiglietti J S (2015) Satellites provide the...
...             | ...
```

Create the reference file from the Excel document and optionally remove any duplicates and sanitise project names from the bib file using the following command. The `remove_duplicates` function allows to remove duplicates from a single file or all files in a given folder. Duplicates can either be entries with the same `ID` or entries with all indentical fields (useful to keep duplicate references associated with different Projects).

```python
python get_references.py
python remove_duplicates.py
python sanitise_project_names.py
```

## Analysis of ESA-IPCC topics : ECVs and references

### Analysis tools
- Run `terms_in_reports.py` to compute and save search terms count for each chapter
- Run `references.py` to extract and save the matching CCI & IPCC references
- Run `references_chapters.py` to add chapter(s) of each matching CCI & IPCC reference
- Run `references_spm.py` to identify matching CCI & IPCC references for each SPM section
- Run `spm_sections.py` to display CCI references and projects supporting SPM statements
- Run `references_text_citations.py` to count in-text citations of CCI references in IPCC reports