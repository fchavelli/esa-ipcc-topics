import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Assuming df is already loaded with the Excel data
df = pd.read_excel('./results/ecvs_in_reports.xlsx')

# Define the report names
reports = ['sr15', 'srccl', 'srocc', 'wg1', 'wg2', 'wg3', 'syr']

def plot_reports_vs_top_ecvs(df, reports, n=10, exclude_sm=False, exclude_a=False):
    # Create a PDF to save the plot
    pdf_path = './plots/reports_vs_top_ecvs.pdf'
    
    # Prepare the plot
    plt.figure(figsize=(15, 8))
    total_width = 0.8
    single_width = total_width / n
    colors = plt.cm.get_cmap('tab20', n)

    # Iterate over each report to plot
    for report_index, report in enumerate(reports):
        report_cols = [col for col in df.columns if col.startswith(report)]
        if exclude_sm:
            report_cols = [col for col in report_cols if 'sm' not in col]
        if exclude_a:
            report_cols = [col for col in report_cols if 'a' not in col]

        df_report = df[['ECV'] + report_cols].copy()
        df_report.set_index('ECV', inplace=True)
        df_numeric = df_report.apply(pd.to_numeric, errors='coerce').fillna(0)
        df_numeric['Total'] = df_numeric.sum(axis=1)
        df_top_n = df_numeric.nlargest(n, 'Total')

        # Plot each of the top n ECVs for this report
        for ecv_index, (ecv, row) in enumerate(df_top_n.iterrows()):
            plt.bar(report_index + ecv_index * single_width, row['Total'], width=single_width, label=ecv if report_index == 0 else "", color=colors(ecv_index))

    plt.xticks(np.arange(len(reports)) + total_width / 2, reports)
    plt.ylabel('Total Mentions')
    plt.title(f'Top {n} Most Cited ECVs per Report')
    plt.legend(title='ECV', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save the plot to the PDF and close the plot
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.close()

    return pdf_path

# Call the function with your parameters
pdf_output_path = plot_reports_vs_top_ecvs(df, reports, n=5, exclude_sm=True, exclude_a=True)
if pdf_output_path:
    print(f"Plot saved to: {pdf_output_path}")
else:
    print("No plot was generated.")
