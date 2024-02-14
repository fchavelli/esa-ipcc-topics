import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Step 1: Read the Excel file
excel_path = './results/ecvs_in_reports.xlsx'
df = pd.read_excel(excel_path)

# Step 2: Define the ECV classification dictionary
with open('./data/cci/ecv_classification.json', 'r') as f:
    ecv_classification = json.load(f)

# Reverse mapping for convenience
ecv_to_category = {}
for category, subcategories in ecv_classification.items():
    for subcategory, ecvs in subcategories.items():
        for ecv in ecvs:
            ecv_to_category[ecv.lower()] = (category, subcategory)  # Assuming ECVs in lowercase for matching

# Step 3: Process DataFrame for classification and adjust column names
# Add classification columns
df['Category'] = df['ECV'].apply(lambda x: ecv_to_category[x.lower()][0] if x.lower() in ecv_to_category else 'Unknown')
df['Subcategory'] = df['ECV'].apply(lambda x: ecv_to_category[x.lower()][1] if x.lower() in ecv_to_category else 'Unknown')

# Reorder DataFrame
columns_order = ['Category', 'Subcategory', 'ECV'] + [col for col in df.columns if col not in ['Category', 'Subcategory', 'ECV']]
df = df[columns_order]

# Adjust column names
df.columns = [col.replace('_', ' ').upper() for col in df.columns]

# Step 4: Plotting
plt.figure(figsize=(10, 8))
# Assuming you want a simple table plot, adjust as needed
ax = plt.subplot(111, frame_on=False)  # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

# Table with color
table = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

# Apply a color range if necessary - this is a placeholder for customization
# Example: color cells based on some criteria

plt.tight_layout()

# Step 5: Save to PDF
pdf_path = './results/search_results_figure.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig()  # saves the current figure into a pdf page
    plt.close()

print(f"PDF saved at {pdf_path}")
