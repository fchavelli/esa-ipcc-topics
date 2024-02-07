#!/bin/bash

# Define the source and target folder paths from the script arguments
SOURCE_FOLDER=$1
TARGET_FOLDER=$2

# Navigate to the parent directory containing preprocess.py
cd "$(dirname "$0")"/..

# Execute the convert_pdf_folder_to_txt function from preprocess.py with the provided arguments
python -c "from preprocess import convert_pdf_folder_to_txt; convert_pdf_folder_to_txt('$SOURCE_FOLDER', '$TARGET_FOLDER')"
