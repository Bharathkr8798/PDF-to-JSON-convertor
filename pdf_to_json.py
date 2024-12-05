""" 
import pdfplumber:Library for extracting text and tables from PDFs.
import fitz: PyMuPDF library for handling PDF documents, including images.
import pytesseract: OCR library for extracting text from images.
from PyPDF2 import PdfReader: Library for extracting metadata and basic text from PDFs.
from PIL import Image: Python Imaging Library for image processing.
import io, os, json, pandas as pd: Standard libraries for byte stream handling, file operations, JSON processing, and data handling with pandas.
"""
import pdfplumber 
import fitz  # PyMuPDF
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
import io
import os
import json
import pandas as pd


# Metadata Extraction
def extract_metadata(pdf_path): # Defines a function to extract metadata from a PDF.
    reader = PdfReader(pdf_path)  # Reads the PDF file using PyPDF2
    metadata = reader.metadata # Extracts metadata from the PDF.
    return {
        "title": metadata.title if metadata and metadata.title else "Unknown Title",
        "author": metadata.author if metadata and metadata.author else "Unknown Author",
        "creation_date": metadata.get('/CreationDate', 'Unknown Date')  
        # Returns a dictionary containing the PDF title, author, and creation date (defaulting to "Unknown" if not present).
    }


# Text Cleaning
def clean_text(text): # Function to clean extracted text.
    cleaned_text = " ".join(text.split())  # Removes extra spaces and formats the text.
    return cleaned_text  #Returns the cleaned text.


# Abstract Table Representation 
def abstract_table_representation(raw_table):     # Converts raw table data into a structured pandas DataFrame.
    if raw_table and len(raw_table) > 1:    #Checks if the table data exists and has content.
        df = pd.DataFrame(raw_table[1:], columns=raw_table[0])  #Converts the raw table into a pandas DataFrame with headers.
        abstract_table = {                  #Converts the DataFrame to a dictionary with column names and rows.
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records")      # Convert each row into a dictionary
        }
        return abstract_table                 # Returns the structured table.
    return {}                 # Return empty dictionary if no valid table is found


# Text, Table, and OCR Extraction
def extract_text_and_tables_and_ocr(pdf_path): # Main function to extract text, tables, and OCR data.
    pages = []
    doc = fitz.open(pdf_path)  # Open the PDF for image extraction
    
    with pdfplumber.open(pdf_path) as pdf:  
        for i, page in enumerate(pdf.pages, start=1):
            # Extract text using pdfplumber
            text = page.extract_text() or ""
            cleaned_text = clean_text(text)
            
            # Extract tables from the page
            tables = []
            for table in page.extract_tables():
                abstract_table = abstract_table_representation(table)
                if abstract_table:
                    tables.append(abstract_table)
            
            # Extract OCR text from images on the current page using pytesseract
            page_doc = doc.load_page(i - 1)  # PyMuPDF pages are zero-indexed
            pix = page_doc.get_pixmap()  # Create a pixmap (image representation of the page)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Use pytesseract to extract text from the image
            raw_text = pytesseract.image_to_string(img)
            
            # Clean up and split OCR text into lines
            lines = raw_text.splitlines()
            ocr_lines = [line.strip() for line in lines if line.strip()]
            
            # Store the extracted data for the current page
            pages.append({
                "page_number": i,
                "text": cleaned_text.strip(),
                "tables": tables if tables else None,  # Store None if no tables exist
                "ocr_text": ocr_lines  # OCR text as a list of cleaned lines
            })
    
    return pages


# Image Extraction
def extract_images_with_fitz(pdf_path, output_folder): # Extract images from the PDF using fitz (PyMuPDF) and save them in the specified folder.
    
    doc = fitz.open(pdf_path) # Opens the PDF with PyMuPDF.
    img_counter = 0

    for i in range(len(doc)):  # Loops through each page of the PDF
        page = doc.load_page(i)
        images = page.get_images(full=True) # Retrieves all images from the page.

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref) # Extracts the raw image data.
            image_bytes = base_image["image"]
            img_mode = base_image.get("colorspace", "Unknown")

            # Create a PIL Image from the byte data
            img = Image.open(io.BytesIO(image_bytes))  # Converts raw image bytes to a PIL image.

            # Convert CMYK to RGB if necessary
            if img.mode == "CMYK":  
                img = img.convert("RGB") 

            # Save the image in the specified folder
            img_path = os.path.join(output_folder, f"image_{img_counter}.png")
            img.save(img_path, format="PNG") # Saves the image as a PNG in the specified folder.
            img_counter += 1
            print(f"Image saved as {img_path} (Mode: {img_mode})")


# Save to JSON
def save_to_json(data, output_file):  # Save the extracted data to a JSON file.
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Main Execution
if __name__ == "__main__":
    pdf_file = "sample.pdf"  # Replace with the path to your PDF file
    output_text_json = "output_of_sample.json"  # Path for the output JSON file
    output_images_folder = "extracted_images_of_sample"  # Folder to store extracted images

    # Create folder to save images if it doesn't exist
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)

    try:
        
        metadata = extract_metadata(pdf_file)  # Extract metadata from the PDF
        print("Metadata:", metadata)
        extracted_text = extract_text_and_tables_and_ocr(pdf_file)  # Extract text, tables, and OCR text from the PDF
        extract_images_with_fitz(pdf_file, output_images_folder)  # Extract images from the PDF
        structured_data = {
            "metadata": metadata,
            "text_and_tables": extracted_text  # pdfplumber extracted text and tables
        }  # Combine extracted data into a structured format
        save_to_json(structured_data, output_text_json)   # Save the combined data into a JSON file
        print(f"Text, tables, and images extracted and saved to {output_text_json}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
