import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Reload the Excel file
df = pd.read_excel('./results/ecvs_in_reports.xlsx')

# Define the report names
reports = ['sr15', 'srccl', 'srocc', 'wg1', 'wg2', 'wg3', 'syr']

def plot_top_ecvs_by_report(df, reports, n=10, exclude_sm=False, exclude_a=False):
    pdf_path = './plots/ecvs_vs_chapters.pdf'
    plots_generated = False
    
    with PdfPages(pdf_path) as pdf:
        for report in reports:
            report_cols = [col for col in df.columns if col.startswith(report) and ((not exclude_sm or 'sm' not in col) and (not exclude_a or 'a' not in col))]

            if not report_cols:
                continue

            # Use a copy to avoid SettingWithCopyWarning
            df_report = df[['ECV'] + report_cols].copy()
            df_report.set_index('ECV', inplace=True)

            # Convert columns to numeric, handling errors
            df_numeric = df_report.apply(pd.to_numeric, errors='coerce').fillna(0)
            df_numeric['Total'] = df_numeric.sum(axis=1)
            
            # Select top n ECVs based on total mentions within the report
            df_top_n = df_numeric.nlargest(n, 'Total')

            # Drop the 'Total' column before plotting
            df_top_n = df_top_n.drop(columns='Total')

            if df_top_n.empty:
                continue

            # Modify column names to improve readability
            modified_columns = [col.split('_', 1)[1].replace('_', ' ').upper() for col in df_top_n.columns if col != 'Total']
            
            plt.figure(figsize=(12, 8))
            df_top_n.plot(kind='bar', legend=True, colormap='viridis')
            plt.title(f"Top {n} ECVs in {report.upper()} Report")
            plt.ylabel('Mentions')
            plt.xticks(rotation=45, ha="right")
            plt.legend(title='Chapter', bbox_to_anchor=(1.05, 1), loc='upper left', labels=modified_columns)
            plt.tight_layout()

            pdf.savefig(bbox_inches='tight')
            plt.close()
            plots_generated = True

    if not plots_generated:
        print("No plots were generated based on the criteria.")
        return None

    return pdf_path

# Example function call
pdf_output_path = plot_top_ecvs_by_report(df, reports, n=10, exclude_sm=True, exclude_a=True)
if pdf_output_path:
    print(f"Plots saved to: {pdf_output_path}")
else:
    print("No plots were generated.")
