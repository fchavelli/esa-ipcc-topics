# Automatic download of WG1,2,3 chapters (.pdf) and references (.bib)
# Manual download is prefered for WG1,2,3 SPMs, TSs and WG1 Atlas (referenced as chapter 13)
# Manual download is prefered for SYR and SR chapters, SPMs and TSs since url naming is not consistent

import requests
import os

# Create downloads directories if they don't exist
download_folder = 'data'
folders = ['data/reports/pdf', 'data/references']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to download a file from a URL
def download_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error on a failed request
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

# Loop through the specified ranges for i and j
for i in range(1, 4):
    # Set the range for j based on the value of i
    j_range = 12 if i == 1 else 18 if i == 2 else 17
    for j in range(1, j_range + 1):
        # Format j with leading zeros
        j_formatted = f"{j:02}"
        # Construct the URL and filename
        chapter_url = f"https://www.ipcc.ch/report/ar6/wg{i}/downloads/report/IPCC_AR6_WG{i*"I"}_Chapter{j_formatted}.pdf"
        filename = os.path.join(download_folder, f"reports/pdf/wg{i}_ch{j}.pdf")
        download_file(chapter_url, filename)
        reference_url = f"https://www.ipcc.ch/report/ar6/wg{i}/downloads/report/IPCC_AR6_WG{i*"I"}_References_Chapter{j_formatted}.bib"
        filename = os.path.join(download_folder, f"references/wg{i}_ch{j}.bib")
        download_file(reference_url, filename)
