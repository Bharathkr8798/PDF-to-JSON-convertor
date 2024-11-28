"""
pdfplumber: A library used for extracting text and tables from PDF files.
json: A standard Python library for working with JSON data, such as parsing, manipulating, and saving JSON.
pandas: A powerful data manipulation library that is useful for working with structured data like tables.
PyPDF2: A library for reading PDF files and extracting metadata and other information, such as the title, author, and creation date.
"""

import pdfplumber
import json
import pandas as pd
from PyPDF2 import PdfReader

# Function: extract_metadata

def extract_metadata(pdf_path):
    """
    Extract metadata such as title and author from the PDF.
    """
    reader = PdfReader(pdf_path)
    metadata = reader.metadata
    return {
        "title": metadata.title if metadata and metadata.title else "Unknown Title",
        "author": metadata.author if metadata and metadata.author else "Unknown Author",
        "date": metadata.get('/CreationDate', 'Unknown Date')  # Extract creation date if available
    }

#Function: clean_text

def clean_text(text):
    """
    Clean up extracted text by removing unwanted characters or formatting.
    """
    # Replace multiple spaces with a single space
    cleaned_text = " ".join(text.split())
    return cleaned_text


#Function: abstract_table_representation

def abstract_table_representation(raw_table):
    """
    Convert raw table data into an abstract representation using pandas.
    """
    if raw_table and len(raw_table) > 1:
        # Ensure the first row is treated as a header
        df = pd.DataFrame(raw_table[1:], columns=raw_table[0])
        abstract_table = {
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records")  # Convert each row to a dictionary
        }
        return abstract_table
    return {}  # Return empty dictionary if no valid table is found


def extract_text_and_tables(pdf_path):
    """
    Extract text and abstract tables from a PDF file.
    """
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            # Extract text
            text = page.extract_text() or ""
            cleaned_text = clean_text(text)
            
            # Extract and abstract tables
            tables = []
            for table in page.extract_tables():
                abstract_table = abstract_table_representation(table)
                if abstract_table:
                    tables.append(abstract_table)
            
            # Store page data, even if there are no tables
            pages.append({
                "page_number": i,
                "text": cleaned_text.strip(),
                "tables": tables if tables else None  # If no tables, store None
            })
    return pages

#Function: generate_jso 

def generate_json(pdf_path):
    """
    Generate a structured JSON from a PDF file.
    """
    metadata = extract_metadata(pdf_path)
    pages = extract_text_and_tables(pdf_path)
    
    # Build the JSON structure
    structured_data = {
        "document_title": metadata["title"],
        "author": metadata["author"],
        "date": metadata["date"],  # Use extracted date from metadata
        "pages": pages
    }
    return structured_data

#Function: save_to_json

def save_to_json(data, output_file):
    """
    Save the JSON data to a file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


#Main Script Execution:

if __name__ == "__main__":
    # Specify input PDF and output JSON paths
    pdf_file = "example3.pdf"  # Replace with your PDF file path
    output_json = "output3.json"
    
    # Extract and save structured data
    try:
        structured_data = generate_json(pdf_file)
        save_to_json(structured_data, output_json)
        print(f"Extracted data saved to {output_json}")
    except Exception as e:
        print(f"Error extracting data from the PDF: {e}")
