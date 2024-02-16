import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import json

# Load ECV classification
ecv_classification_path = './data/cci/ecv_classification.json'
with open(ecv_classification_path, 'r') as file:
    ecv_classification = json.load(file)

# Adjust the color map for better distinction between "ocean" and "atmosphere"
group_colors = {
    'atmosphere': '#29B6F6',  # Slightly lighter blue for the atmosphere
    'land': '#4CAF50',        # Rich, earthy green for land
    'ocean': '#1976D2'        # Slightly darker blue for the ocean
}

# Flatten the classification for easier access
ecv_to_group = {}
for group, categories in ecv_classification.items():
    for category, ecvs in categories.items():
        for ecv in ecvs:
            ecv_to_group[ecv.lower()] = group

def create_and_save_colored_plot_from_excel(excel_path, pdf_path, min_occurrences=0):
    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Aggregate mentions across all chapters for each item
    df['Total Mentions'] = df.iloc[:, 1:].sum(axis=1)

    # Filter out ECVs with occurrences less than min_occurrences and create a copy to avoid the warning
    df_filtered = df[df['Total Mentions'] >= min_occurrences].copy()

    # Capitalize the first letter of each ECV
    df_filtered['ECV'] = df_filtered['ECV'].str.title()

    # Sort the data based on total mentions to make the plot easier to understand
    df_sorted = df_filtered.sort_values(by='Total Mentions', ascending=False)

    # Map each ECV to its group color
    df_sorted['Color'] = df_sorted['ECV'].apply(lambda ecv: group_colors[ecv_to_group.get(ecv.lower(), 'atmosphere')])

    # Plot with mentions on the y-axis and ECVs on the x-axis
    plt.figure(figsize=(12, 10))  # Adjusted for potential increase in ECV labels
    bars = plt.bar(df_sorted['ECV'], df_sorted['Total Mentions'], color=df_sorted['Color'])

    # Rotate ECV names for better readability
    plt.xticks(rotation=45, ha="right")

    # Create a legend for the colors used
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=group_colors[group], label=group.title()) for group in group_colors]
    plt.legend(handles=legend_elements, title="ECV Categories")

    plt.ylabel('Total Mentions')
    plt.title('Total Mentions of ECVs Across Chapters')
    plt.tight_layout()  # Adjust layout to not cut off labels

    # Save the plot to a PDF file
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(bbox_inches='tight')
    plt.close()

# Example usage
min_occurrences = 100  # Set your minimum occurrences threshold here
excel_path = './results/ecvs_in_reports.xlsx'  # Use the actual Excel file path
pdf_path = f'./plots/ecvs_in_reports_colored_plot_min{min_occurrences}.pdf'  # Desired PDF file path

create_and_save_colored_plot_from_excel(excel_path, pdf_path, min_occurrences)
