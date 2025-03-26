import pdfplumber  # For extracting text from PDF
import os  # For file and path operations
import time  # For simple animation
import argparse  # For command-line argument parsing
from tqdm import tqdm  # For progress bar
import pandas as pd  # For handling table conversion

def extract_table_markdown(table):
    """
    Convert extracted table data into Markdown table format.
    """
    if not table:
        return ""
    
    # Ensure all elements in the table are strings, replace None with ""
    table = [[cell if cell is not None else "" for cell in row] for row in table]

    markdown_table = "| " + " | ".join(table[0]) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(table[0])) + " |\n"
    
    for row in table[1:]:
        markdown_table += "| " + " | ".join(row) + " |\n"
    
    return markdown_table + "\n"

def pdf_to_md(pdf_path, output_path):
    """
    Extracts text and tables from a PDF file and saves it as a Markdown (.md) file.

    Args:
        pdf_path (str): Path to the PDF file to be converted.
        output_path (str): Path where the Markdown file will be saved.
    """

    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        print("Error: PDF file not found!")
        return
    
    # If output_path is a directory, generate a default filename
    if os.path.isdir(output_path):
        pdf_name = os.path.basename(pdf_path).replace(".pdf", ".md")
        output_path = os.path.join(output_path, pdf_name)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("\n[INFO] Starting conversion...")

    # Loading animation simulation
    loading_animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(10):
        print(f"\r{loading_animation[_ % len(loading_animation)]} Processing PDF file...", end="", flush=True)
        time.sleep(0.1)

    # Open PDF and create a Markdown file
    with pdfplumber.open(pdf_path) as pdf, open(output_path, "w", encoding="utf-8") as md_file:
        total_pages = len(pdf.pages)

        # Show progress bar with tqdm
        for i, page in enumerate(tqdm(pdf.pages, desc="Converting pages", unit="page")):
            text = page.extract_text()
            tables = page.extract_tables()
            
            md_file.write(f"# Page {i + 1}\n\n")  # Page title
            
            if text:
                md_file.write(text + "\n\n")  # Page content
            
            if tables:
                for table in tables:
                    md_file.write("## Table\n\n")
                    md_file.write(extract_table_markdown(table))
                    md_file.write("\n\n")
            
            md_file.write("---\n\n")  # Page separator

    print("\n✅ Conversion complete! Markdown file saved at:", output_path)

# Command-line argument parser
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a PDF file to Markdown format. Usage: python pdf_to_md.py -I [input_path] -O [output_path]"
    )
    parser.add_argument("-I", "--input", required=True, help="Path to the input PDF file.")
    parser.add_argument("-O", "--output", required=True, help="Path to the output Markdown file or directory.")
    args = parser.parse_args()

    pdf_to_md(args.input, args.output)
