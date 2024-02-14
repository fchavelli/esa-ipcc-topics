import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Ensure paths are correctly specified for your environment
excel_path = './results/ecvs_in_reports.xlsx'
classification_path = './data/cci/ecv_classification.json'

# Load ECV classification
with open(classification_path, 'r') as f:
    ecv_classification = json.load(f)

# Create reverse mapping for ECVs to categories and subcategories
ecv_to_category = {}
for category, subcategories in ecv_classification.items():
    for subcategory, ecvs in subcategories.items():
        for ecv in ecvs:
            ecv_to_category[ecv.lower()] = (category, subcategory)

# Load the Excel file
df = pd.read_excel(excel_path)

# Check if 'ECV' column exists and then assign 'Category' and 'Subcategory'
if 'ECV' in df.columns:
    df['Category'] = df['ECV'].apply(lambda x: ecv_to_category.get(x.lower(), ('Unknown', 'Unknown'))[0])
    df['Subcategory'] = df['ECV'].apply(lambda x: ecv_to_category.get(x.lower(), ('Unknown', 'Unknown'))[1])
else:
    raise KeyError("'ECV' column not found in DataFrame.")

# Ensure 'Category' and 'Subcategory' columns are added
if 'Category' not in df.columns or 'Subcategory' not in df.columns:
    raise KeyError("Failed to add 'Category' and 'Subcategory' columns.")

if 'Value' not in df.columns:
    df['Value'] = 1  # This is a placeholder. In practice, replace this with your actual data logic.

# Proceed with the pivot_table creation
pivot_table = pd.pivot_table(df, index='Category', columns='Subcategory', values='Value', fill_value=0)

# Visualization with seaborn
plt.figure(figsize=(12, 9))
sns.set_theme()
sns.heatmap(pivot_table, annot=True, cmap="YlGnBu")

plt.tight_layout()

# Save to PDF
pdf_path = './results/heatmap_search_results_figure.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig()
    plt.close()

print(f"PDF saved at {pdf_path}")