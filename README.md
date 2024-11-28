
To run this python code, you need to install the following Python libraries:

**pdfplumber:**
pip install pdfplumber

**PyPDF2:**
pip install PyPDF2

**pandas:**
pip install pandas

steps:
1. Ensure you have Python installed (preferably version 3.7 or higher). Install the required libraries using the commands mentioned above.
2. Place the PDF file you want to process in the same directory as the script, or provide the correct file path to the pdf_file variable in the script.
3. Save the script in a Python file (e.g., pdf-json-m.py) and execute it from the command line or terminal.
4. After successful execution, the script will generate a JSON file (output.json) containing the extracted metadata, text, and table data.


This Python script is designed to extract text, metadata, and table data from a PDF file and save it in a structured JSON format. 

Explanation of the Code
Library Imports:

1. pdfplumber: Used to extract text and table data from PDF pages.
2. json: Converts Python objects into JSON format and saves them to a file.
3. pandas: Handles tabular data, including processing and abstracting tables extracted from the PDF.
4. PyPDF2: Extracts metadata (like title, author, creation date) from the PDF.


Key Functions:

.extract_metadata(pdf_path): Extracts metadata such as title, author, and creation date from the PDF using PyPDF2.
.clean_text(text): Cleans extracted text by removing extra spaces and unwanted formatting.
.abstract_table_representation(raw_table): Converts raw table data (extracted by pdfplumber) into a dictionary format with column names and rows, leveraging pandas.
.extract_text_and_tables(pdf_path): Processes each page of the PDF to extract cleaned text and any tables present. The function iterates through each page and uses pdfplumber to extract text and table data.
.generate_json(pdf_path): Combines the metadata and the page-by-page text and table data into a structured format suitable for JSON output.
.save_to_json(data, output_file): Writes the structured data to a specified JSON file.

Main Execution:

Specifies the input PDF (example.pdf) and output JSON file (output.json).
Calls the extraction functions to process the PDF and save the resulting structured data in JSON format.
