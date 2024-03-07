# Automatic download of AR6 and AR5 WG1,2,3 chapters (.pdf), AR4 WG2,3 chapters and AR6 references (.bib)
# Manual download is prefered for WG1,2,3 SPMs, TSs (and WG1 Atlas for AR6, referenced as chapter 13)
# Manual download is prefered for SYR and SR chapters, SPMs and TSs since url naming is not consistent

import requests
import os

# AR of interest
ar = 4

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

if ar == 6:

    download_folder = 'data'
    folders = ['data/reports/pdf', 'data/references']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

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

if ar == 5:

    download_folder = 'data'
    folder = f'{download_folder}/reports/pdf/ar5'
    if not os.path.exists(folder):
            os.makedirs(folder)

    # Loop through the specified ranges for i and j
    for i in range(1, 4):
        # Set the range for j based on the value of i
        j_range = 14 if i == 1 else 30 if i == 2 else 16
        for j in range(1, j_range + 1):
            # Format j with leading zeros
            j_formatted = f"{j:02}"
            # Construct the URL and filename
            if i == 1:
                if j not in [1,2]:
                    chapter_url = f'https://www.ipcc.ch/site/assets/uploads/2018/02/WG1AR5_Chapter{j_formatted}_FINAL.pdf'
                else:
                    chapter_url = f'https://www.ipcc.ch/site/assets/uploads/2017/09/WG1AR5_Chapter{j_formatted}_FINAL.pdf'
            if i == 2:
                chapter_url = f'https://www.ipcc.ch/site/assets/uploads/2018/02/WGIIAR5-Chap{j}_FINAL.pdf'
            if i == 3:
                chapter_url = f'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_chapter{j}.pdf'
            filename = os.path.join(download_folder, f"reports/pdf/ar5/wg{i}_ch{j}.pdf")
            download_file(chapter_url, filename)

if ar == 4:

    download_folder = 'data'
    folder = f'{download_folder}/reports/pdf/ar4'
    if not os.path.exists(folder):
            os.makedirs(folder)

    # Loop through the specified ranges for i and j
    for i in range(2, 4):
        # Set the range for j based on the value of i
        j_range = 20 if i == 2 else 13
        for j in range(1, j_range + 1):
            # Format j with leading zeros
            j_formatted = f"{j:02}"
            # Construct the URL and filename
            chapter_url = f'https://www.ipcc.ch/site/assets/uploads/2018/02/ar4-wg{i}-chapter{j}-1.pdf'
            filename = os.path.join(download_folder, f"reports/pdf/ar4/wg{i}_ch{j}.pdf")
            download_file(chapter_url, filename)
