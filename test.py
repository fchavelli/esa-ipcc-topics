import pandas as pd

def sort_columns(df):
    ecv_column = df['ECV'] if 'ECV' in df.columns else None
    def sort_key(col):
        if 'ch' in col:
            num_part = int(''.join(filter(str.isdigit, col.split('ch')[-1])))
            return (0, num_part)
        elif 'a' not in col:
            return (1, col)
        else:
            return (2, col)
    columns_to_sort = [col for col in df.columns if col != 'ECV']
    sorted_columns = sorted(columns_to_sort, key=sort_key)
    if ecv_column is not None:
        sorted_columns = ['ECV'] + sorted_columns
    return df[sorted_columns]

input_excel_path = './results/ecvs_in_reports.xlsx'  # Actual input file path
output_excel_path = './results/ecvs_in_reports_edited.xlsx'  # Actual output file path

with pd.ExcelWriter(output_excel_path) as writer:
    for sheet_name in pd.ExcelFile(input_excel_path).sheet_names:
        df = pd.read_excel(input_excel_path, sheet_name=sheet_name)
        df_sorted = sort_columns(df)
        df_sorted.to_excel(writer, sheet_name=sheet_name, index=False)