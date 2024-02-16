import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

df = pd.read_excel('./results/ecvs_in_reports.xlsx')

# Define the report names
reports = ['sr15', 'srccl', 'srocc', 'wg1', 'wg2', 'wg3', 'syr']

def plot_chapters_vs_ecvs_side_by_side(df, reports, n=10, exclude_sm=False, exclude_a=False):
    pdf_path = './plots/chapters_vs_ecvs.pdf'
    plots_generated = False
    
    with PdfPages(pdf_path) as pdf:
        for report in reports:
            report_cols = [col for col in df.columns if col.startswith(report) and ((not exclude_sm or 'sm' not in col) and (not exclude_a or 'a' not in col))]
            
            if not report_cols:
                continue

            df_report = df[['ECV'] + report_cols].copy()
            df_report.set_index('ECV', inplace=True)

            df_numeric = df_report.apply(pd.to_numeric, errors='coerce').fillna(0)
            df_numeric['Total'] = df_numeric.sum(axis=1)
            df_top_n = df_numeric.nlargest(n, 'Total').drop(columns='Total')

            if df_top_n.empty:
                continue

            df_transposed = df_top_n.T
            simplified_columns = [col.split('_', 1)[1].replace('_', ' ').upper() for col in df_transposed.index]
            df_transposed.index = simplified_columns

            plt.figure(figsize=(12, 8))
            # Create a side by side bar plot
            bar_width = 0.8 / n  # Width of bars in the bar plot
            indices = np.arange(len(df_transposed.index))  # X-axis positions for groups of bars
            
            for i, ecv in enumerate(df_top_n.index):
                plt.bar(indices + i * bar_width, df_transposed[ecv], width=bar_width, label=ecv)

            plt.title(f"Top {n} ECVs in {report.upper()} chapters")
            plt.xlabel('Chapters')
            plt.ylabel('Mentions')
            plt.xticks(indices + bar_width * (n - 1) / 2, df_transposed.index, rotation=45, ha="right")
            plt.legend(title='ECV', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            pdf.savefig(bbox_inches='tight')
            plt.close()
            plots_generated = True

    if not plots_generated:
        print("No plots were generated based on the criteria.")
        return None

    return pdf_path

# Call the function with your parameters
pdf_output_path = plot_chapters_vs_ecvs_side_by_side(df, reports, n=5, exclude_sm=True, exclude_a=True)
if pdf_output_path:
    print(f"Plots saved to: {pdf_output_path}")
else:
    print("No plots were generated.")
