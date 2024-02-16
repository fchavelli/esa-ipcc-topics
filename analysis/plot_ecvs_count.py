# This Python script is designed to visualize the occurrence of Essential Climate Variables (ECVs)
# across various chapters of environmental reports. It reads data from an Excel file, aggregates 
# the mentions of ECVs, and filters based on a specified minimum occurrence threshold. The script 
# capitalizes the first letter of each ECV for consistency and visual appeal. ECVs are categorized 
# into groups such as "atmosphere," "land," and "ocean," with each group represented by a specific 
# color in the bar chart. The chart plots ECVs on the horizontal axis and their total mentions on 
# the vertical axis, with ECV names rotated for readability. A legend is included to describe the 
# color coding of categories, enhancing the chart's interpretability. The functionality allows for 
# customization of the minimum occurrences filter to focus the visualization on more frequently 
# mentioned ECVs. The final plot is saved as a PDF file, providing a clear and informative visual 
# summary of the data.

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
    plt.title(f'ECVs count with more than {min_occurrences} occurences across AR6 reports')
    plt.tight_layout()  # Adjust layout to not cut off labels

    # Save the plot to a PDF file
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(bbox_inches='tight')
    plt.close()

# Example usage
min_occurrences = 100  # Set your minimum occurrences threshold here
excel_path = './results/ecvs_in_reports.xlsx'  # Use the actual Excel file path
pdf_path = f'./plots/ecvs_count_min{min_occurrences}.pdf'  # Desired PDF file path

create_and_save_colored_plot_from_excel(excel_path, pdf_path, min_occurrences)
