import os

def process_files(source_folder, before_references_folder, after_references_folder):
    # Ensure target folders exist
    if not os.path.exists(before_references_folder):
        os.makedirs(before_references_folder)
    if not os.path.exists(after_references_folder):
        os.makedirs(after_references_folder)

    files_processed = 0
    files_with_references = 0
    files_without_references = 0
    errors = 0

    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".txt"):
            try:
                print(f"Processing file: {filename}")
                with open(os.path.join(source_folder, filename), 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Find the last occurrence of "References"
                reference_index = content.rfind("References")
                
                if reference_index != -1:
                    content_before_references = content[:reference_index]
                    content_after_references = content[reference_index:]
                    files_with_references += 1

                    # Write content before "References" to a new file in before_references_folder
                    with open(os.path.join(before_references_folder, filename), 'w', encoding='utf-8') as new_file_before:
                        new_file_before.write(content_before_references)
                    
                    # Write content after "References" to a new file in after_references_folder
                    with open(os.path.join(after_references_folder, filename), 'w', encoding='utf-8') as new_file_after:
                        new_file_after.write(content_after_references)
                else:
                    print(f"No 'References' tag found in {filename}.")
                    files_without_references += 1
                    # Optionally, copy the file to both folders or handle differently
                    continue  # Skip this file
                
                files_processed += 1
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                errors += 1
                continue

    # Display summary of actions
    print(f"Summary of actions:")
    print(f"Files processed: {files_processed}")
    print(f"Files with 'References' processed: {files_with_references}")
    print(f"Files without 'References': {files_without_references}")
    print(f"Errors encountered: {errors}")

# Example usage
source_folder = './data/reports/txt'
before_references_folder = './data/reports/content'
after_references_folder = './data/reports/references'
process_files(source_folder, before_references_folder, after_references_folder)
