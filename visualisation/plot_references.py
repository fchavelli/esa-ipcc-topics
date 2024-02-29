import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure the plots directory exists
plots_dir = './plots/projects'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

def process_excel_sheets(excel_path, hide_unwanted_projects=True):
    # Load the Excel file
    xl = pd.ExcelFile(excel_path)
    
    # Dictionary to keep track of total project counts across all sheets
    total_project_counts = {}
    
    for sheet_name in xl.sheet_names:
        # Read each sheet
        df = xl.parse(sheet_name)
        
        # Ensure 'project' column exists
        if 'project' in df.columns:
            # Filter projects, if necessary
            if hide_unwanted_projects:
                df = df[~df['project'].str.contains('lpf|Slbc', case=False, na=False)]
            
            # Count occurrences of each project, excluding empty strings
            project_counts = df['project'].value_counts().drop('', errors='ignore')
            
            # Update total counts
            for project, count in project_counts.items():
                total_project_counts[project] = total_project_counts.get(project, 0) + count
            
            # Sort projects in the sheet plot
            project_counts.sort_values(ascending=False, inplace=True)
            
            # Plot for each sheet
            plt.figure(figsize=(10, 6))
            project_counts.plot(kind='bar', color='skyblue')
            plt.title(f"Count of CCI projects references in {sheet_name.upper()} references")
            plt.ylabel('Count')
            plt.xlabel('CCI Projects')
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            # Save the plot
            plt.savefig(f"{plots_dir}/count_references_{sheet_name}.pdf")
            plt.close()
        
    # Prepare overall plot with projects sorted in decreasing order
    total_project_counts = pd.Series(total_project_counts).sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    total_project_counts.plot(kind='bar', color='skyblue')
    plt.title("Count of CCI project references among AR6 references")
    plt.ylabel('Count')
    plt.xlabel('CCI Projects')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{plots_dir}/count_references_ar6.pdf")
    plt.close()
    
    print(f"Plots are saved in: {plots_dir}")

# Example usage
process_excel_sheets('./results/matched_references.xlsx')
