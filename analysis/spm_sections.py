"""
Input:
- Multisheet spreadsheet containing SPM sections ID, content, references to report sections, and CCI references supporting each report section
- Multisheet spreadsheet containing CCI references metadata (First Author, Title, Year, Journal, DOI) as well as CCI Project(s)

Output:
- PDF document with custom header displaying each SPM sections with its ID, content, references to report section and CCI references with associated projects
"""

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

def format_citations(doi_list, ref_df):
    """Generate formatted citation strings based on DOI matches, using the first author and appending 'et al.'."""
    formatted_citations = []
    for doi in doi_list:
        match = ref_df[ref_df['DOI'] == doi]
        if not match.empty:
            for _, row in match.iterrows():
                citation = f"• {row['First Author']} et al. ({row['Year']}), {row['Title']}, <i>{row['Journal']}</i>, DOI: {row['DOI']} ({row['Project']})"
                formatted_citations.append(citation)
    return formatted_citations

def count_projects(citations):
    """Count the occurrences of each non-null project in citations, handling multiple projects per citation."""
    project_counts = {}
    for citation in citations:
        project_string = citation.split('(')[-1].strip(')')
        projects = project_string.split(", ")
        for project in projects:
            if project:  # Ensure non-empty project string
                project_counts[project] = project_counts.get(project, 0) + 1
    return ", ".join([f"{proj} ({count})" for proj, count in project_counts.items()])

def create_pdf(data_file, ref_file, output_file):
    df = pd.read_excel(data_file)
    ref_df = pd.read_excel(ref_file, sheet_name='wg1')
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Define styles
    title_style = ParagraphStyle('TitleStyle', parent=styles['Title'], alignment=TA_CENTER, fontSize=16, spaceAfter=20)
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Title'], alignment=TA_CENTER, fontSize=14, spaceAfter=20)
    justified_style = ParagraphStyle('Justified', parent=styles['BodyText'], alignment=TA_JUSTIFY, spaceBefore=6, spaceAfter=6)
    header_style = styles['Heading1']

    # Define a style for the content box
    box_style = TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.white)
    ])

    # Add title and subtitle
    story.append(Paragraph("ESA Climate Change Initiative Project publications supporting IPCC AR6 WG1 SPM statements", title_style))
    story.append(Paragraph("Mapping CCI references and projects in WG1 sections supporting SPM statements", subtitle_style))
    #story.append(Paragraph("Analysis of 85 ESA CCI references appearing in IPCC AR6 WG1 report sections supporting SPM statements. Each reference is tagged with one or several CCI project(s).", justified_style))

    for index, row in df.iterrows():
        story.append(Paragraph(f"<b>{row['SPM section']}</b>", header_style))
        story.append(Spacer(1, 12))

        # Content within a thin black square
        content_data = [[Paragraph(f"{row['Content']}", justified_style)]]
        content_table = Table(content_data, colWidths=[450], style=box_style)
        story.append(content_table)
        
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"<b>Report sections</b>: {row['Report sections']}", justified_style))
        story.append(Spacer(1, 12))

        # Normalize DOIs and format citations
        dois = [doi.strip() for doi in str(row['CCI references']).split(';')]
        formatted_citations = format_citations(dois, ref_df)

        # Calculate and display project counts
        project_counts = count_projects(formatted_citations)
        if project_counts:
            story.append(Paragraph(f"<b>CCI Projects:</b> {project_counts}", justified_style))
            story.append(Spacer(1, 12))

        if formatted_citations:
            story.append(Paragraph("<b>CCI references:</b>", justified_style))
            for citation in formatted_citations:
                story.append(Paragraph(citation, justified_style))
        else:
            story.append(Paragraph("No CCI reference found", justified_style))

        story.append(Spacer(1, 24))

    doc.build(story)
    print(f"Processed document saved to {output_file}")

# File paths
data_file = './results/cci_references_spm_sections.xlsx'
ref_file = './data/cci/matched_references_unique_curated.xlsx'
output_file = './results/cci_references_spm_sections.pdf'

# Generate PDF
create_pdf(data_file, ref_file, output_file)
