import pdfplumber
import re
import os

def extract_metadata(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page_text = pdf.pages[0].extract_text()
        
        # 1. year (fiscal year)
        year_match = re.search(r'FY\s*(\d{4})[-–](\d{2,4})', first_page_text, re.IGNORECASE)
        if year_match:
            year = year_match.group(1) + "-" + year_match.group(2)
        else:
            year = None
        
        # 2. region / state name
        region_match = re.search(r'(Odisha|Maharashtra|Kerala|Gujarat|Punjab|Tamil Nadu|Bihar|Assam)', first_page_text, re.IGNORECASE)
        if region_match:
            region = region_match.group(1)
        else:
            region = None
        
        # 3. regulatory body name
        regulator_match = re.search(r'([A-Z][A-Za-z\s]+ELECTRICITY REGULATORY COMMISSION)', first_page_text)
        if regulator_match:
            regulatory_body = regulator_match.group(1)
        else:
            regulatory_body = None
        
        # 4. order date
        date_match = re.search(r'DATE OF ORDER\s*[:\-]?\s*(\d{2}[./-]\d{2}[./-]\d{4})', first_page_text, re.IGNORECASE)
        if date_match:
            order_date = date_match.group(1)
        else:
            order_date = None
        
        metadata = {
            "year": year,
            "region": region,
            "regulatory_body": regulatory_body,
            "order_date": order_date
        }
        return metadata

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    PDF_PATH = os.path.join(BASE_DIR, "data", "DISCOM_TARIFF_ORDER_FY_2023-24.pdf")
    
    metadata = extract_metadata(PDF_PATH)
    print("✅ Extracted Metadata:")
    print(metadata)
