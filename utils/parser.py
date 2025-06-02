import os
import logging
from pdfminer.high_level import extract_text

# Suppress noisy PDFMiner warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)

def extract_text_from_txt(filepath):
    """
    Reads plain text from a .txt file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Failed to read TXT file {filepath}: {e}")
        return ""

def extract_text_from_pdf(filepath):
    """
    Extracts text content from a PDF file using pdfminer.
    """
    try:
        return extract_text(filepath)
    except Exception as e:
        print(f"❌ Failed to extract PDF {filepath}: {e}")
        return ""

def extract_text_from_file(filepath):
    """
    Dispatches file to the appropriate parser based on file extension.
    """
    if filepath.endswith('.txt'):
        return extract_text_from_txt(filepath)
    elif filepath.endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    else:
        print(f"⚠️ Unsupported file type: {filepath}")
        return ""
