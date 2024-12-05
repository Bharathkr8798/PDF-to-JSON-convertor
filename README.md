Python libraries

The script uses several Python libraries. Here's the list of libraries to install:

1. pdfplumber (for extracting text and tables from PDFs)
2. PyMuPDF (fitz) (for working with PDF images and metadata)
3. pytesseract (for OCR text extraction from images)
4. PyPDF2 (for extracting metadata)
5. Pillow (PIL) (for image processing)
6. pandas (for handling tabular data)
7. os, io, and json (built-in Python libraries; no installation needed)

Use pip to install the required libraries. Run these commands in your terminal/command prompt:

> pip install pdfplumber pymupdf pytesseract PyPDF2 pillow pandas

pytesseract requires Tesseract OCR to be installed separately on your system.

1. Install Tesseract: On Windows: Download the installer from Tesseract GitHub Releases and install it.
2. Configure pytesseract: After installing Tesseract, ensure tesseract.exe is added to your system's PATH (on Windows). You may need to specify its path in your script:

> pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Example path

Preparing the Environment
1. Create a folder for the script and place your PDF file (example1.pdf) in it.
2. Create another folder named extracted_images_of_example1 (or let the script create it automatically).

Output
1. Extracted text, metadata, and tables will be saved in output_of_example1.json.
Images Folder:
2. Extracted images will be saved in the extracted_images_of_example1 folder.


