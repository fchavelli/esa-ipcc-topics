# esa-ipcc-topics
Analysis of ESA Climate Office topics across last IPCC reports

Create a python virtual environment and install the dependencies.

Using PowerShell

```PowerShell
python -m venv env
.\env\Scripts\Activate
pip install -r requirements.txt
```

Using bash

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Download the available reports (.pdf) and references (.bib) from the IPCC website.
AR6 WG1,2,3 chapters and associated references can be downloaded using the following command.

```python
python get_data.py
```

Other files including Special Reports and Synthesis Report chapters, SPMs, TSs and their references can be downloaded manually from the [IPCC website](https://www.ipcc.ch).

Once pdf files are downloaded, they can be converted to txt files using the following command

```bash
./scripts/run_conversion.sh data/ipcc/reports/pdf data/ipcc/reports/txt