import pandas as pd

# Function to normalize and expand data separated by '| ' or ';'
def normalize_data(data_frame, column_name):
    # Determine the separator based on the column
    separator = ';' if column_name in ['Topic cluster name', 'Topic name'] else '|'
    
    # Split and normalize the data based on the separator
    return (
        data_frame.drop(column_name, axis=1)
        .join(
            data_frame[column_name].str.split(separator, expand=True)
            .stack()
            .reset_index(level=1, drop=True)
            .rename(column_name)
        )
    ).reset_index(drop=True)

# Read the XLSX file
df = pd.read_excel('./data/cci/scival.xlsx')

# Normalize each column that needs splitting
columns_to_normalize = ['Authors', 'Institutions', 'Country/Region', 'Topic Cluster name', 'Topic name']
for column in columns_to_normalize:
    df = normalize_data(df, column)

# Create unique tables for each entity
entities = ['Authors', 'Institutions', 'Country/Region', 'Topic Cluster name', 'Topic name']
entity_tables = {}
for entity in entities:
    entity_tables[entity] = df[[entity, 'DOI']].drop_duplicates().reset_index(drop=True)
    entity_tables[entity]['ID'] = entity_tables[entity].index + 1

# Generate join tables mapping DOI to other entities' IDs
join_tables = {}
for entity, table in entity_tables.items():
    join_table_name = f'Paper{entity.replace(" ", "")}'
    join_tables[join_table_name] = table[['DOI', 'ID']].rename(columns={'ID': f'{entity}ID'})

# Write everything to a new XLSX file
with pd.ExcelWriter('./results/matching_references_scival.xlsx', engine='openpyxl') as writer:
    for entity, table in entity_tables.items():
        # Sanitize the sheet name by replacing invalid characters
        sanitized_sheet_name = entity.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('[', '_').replace(']', '_')
        table.drop('DOI', axis=1).to_excel(writer, sheet_name=sanitized_sheet_name, index=False)
    for join_table_name, table in join_tables.items():
        # Similarly sanitize join table names
        sanitized_join_table_name = join_table_name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('[', '_').replace(']', '_')
        table.to_excel(writer, sheet_name=sanitized_join_table_name, index=False)

print("Normalization and export completed successfully.")

