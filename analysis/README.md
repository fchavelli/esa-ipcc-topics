# Analysis of ESA-IPCC topics : ECVs and references

## Analysis
- Run `terms_in_reports.py` to compute and save search terms count for each chapter
- Run `references.py` to extract and save the matching CCI & IPCC references
- Run `references_chapters.py` to add chapter(s) of each matching CCI & IPCC reference
- Run `references_spm.py` to identify matching CCI & IPCC references for each SPM section
- Run `spm_sections.py` to display CCI references and projects supporting SPM statements
- Run `references_text_citations.py` to count in-text citations of CCI references in IPCC reports

## Deprecated

### Visualisation
Several tools allow to present the data:

#### ECVs
- ECVs count in all AR6 reports: `plot_ecvs_count.py`
- Top ECVs count in each AR6 chapter: `plot_chapters_vs_ecvs.py` or `plot_ecvs_vs_chapters.py`
- Top ECVs count in each AR6 reports: `plot_reports_vs_ecvs.py`

#### References
- Count of CCI Projects in matching CCI-IPCC references: `plot_references.py`

#### Details

##### ECVs count
The list of ECVs is defined in `cci_topics.py` together with their categories and aliases. It is saved in a json document for analysis and in an Excel document for display.