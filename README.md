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

Data is organized as follows:

```
\data
    \cci            [cci references (.xlsx) and topics (.py)]
    \reports
        \pdf        [ipcc report files (.pdf)]
        \txt        [ipcc report files (.txt)]
    \references     [esa & ipcc references (.bib)]
```

Download the available reports (.pdf) and references (.bib) from the IPCC website.
AR6 WG1,2,3 chapters and associated references can be downloaded automatically using the following command.

```
python download_reports.py
```

Other files including Special Reports (SR) and Synthesis Report (SYR) chapters, Summary for Policymakers (SPM), Technical Summaries (TS), Annexes (A) as well as references can be downloaded manually from the [IPCC website](https://www.ipcc.ch).

## Preprocessing

Once pdf files are downloaded, they can be converted to txt files using the following command. The text in tables and figures are read when available (e.g. WG1 Chapter 1, Fig 1.1).

```bash
scripts/pdf_to_txt.sh ../data/reports/pdf ../data/reports/txt
```

Download the CCI references (.bib) or build a bibliography from an Excel file (containing at least a title or a doi for each reference). Reference metadata (including type, date, authors, journal, and doi) will be recovered online using Crossref API. The Excel file is expected to have the following structure with no empty rows.

```
Project         | Reference
Soil moisture   | Nitta Tomoko (2017) Impact of Arctic Wetlands...
Sea level       | Famiglietti J S (2015) Satellites provide the...
...             | ...
```

Create the reference file from the Excel document and optionally remove any duplicates and sanitise project names from the bib file using the following command.

```python
python get_references.py
python remove_duplicates.py
python sanitise_project_names.py
```

Create ECV objects with names, associated CCI project, custom search terms, aliases, displays etc in `cci_topics.py` and run the following command to create objects.

```python
python ./utils/ecvs.py
```