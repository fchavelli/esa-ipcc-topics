import os
from PyPDF2 import PdfReader

def convert_pdf_folder_to_txt(source_folder, target_folder):
    # Check if the target folder exists, if not, create it
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    # List all PDF files in the source folder
    pdf_files = [f for f in os.listdir(source_folder) if f.endswith('.pdf')]
    
    # Process each PDF file
    for i, pdf_file in enumerate(pdf_files):
        source_path = os.path.join(source_folder, pdf_file)
        target_path = os.path.join(target_folder, pdf_file.replace('.pdf', '.txt'))
        
        # Initialize a PDF reader and open the source PDF file
        reader = PdfReader(source_path)
        
        # Extract text from each page and attempt to write to a new txt file
        with open(target_path, 'w', encoding='utf-8') as txt_file:
            for page in reader.pages:
                try:
                    text = page.extract_text()
                    if text:
                        txt_file.write(text)
                except UnicodeEncodeError as e:
                    print(f"Encoding error encountered and skipped in {pdf_file}: {e}")
        
        # Display progress
        print(f"Converted ({i+1}/{len(pdf_files)}): {pdf_file} to txt")
        
    print("Conversion completed.")


source_folder = './data/reports/pdf'
target_folder = './data/reports/txt'

source_folder = './data/reports/pdf/full_temp'
target_folder = './data/reports/full'

convert_pdf_folder_to_txt(source_folder, target_folder)