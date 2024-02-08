# ESA Climate Office - IPCC analysis
Analysis of ESA Climate Office topics across last IPCC reports

## Installation

Create a python virtual environment and install the dependencies.

PowerShell

```PowerShell
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
    \reports
        \pdf        [ipcc report files in .pdf format]
        \txt        [ipcc report files in .txt format]
    \references     [ipcc references in .bib format]
```

Download the available reports (.pdf) and references (.bib) from the IPCC website.
AR6 WG1,2,3 chapters and associated references can be downloaded automatically using the following command.

```python
python get_data.py
```

Other files including Special Reports and Synthesis Report chapters, SPMs, TSs and their references can be downloaded manually from the [IPCC website](https://www.ipcc.ch).

Once pdf files are downloaded, they can be converted to txt files using the following command.

```bash
./scripts/run_conversion.sh data/reports/pdf data/reports/txt
```

Download the CCI references (.bib) or build a new bibliography from an raw Excel file (containing at least reference titles) using the following command.

```python
python get_bib.py
```