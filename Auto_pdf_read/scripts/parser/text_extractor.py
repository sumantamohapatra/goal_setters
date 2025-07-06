import pdfplumber
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "data", "DISCOM_TARIFF_ORDER_FY_2023-24.pdf")


def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_pages = []
        for page in pdf.pages[0:5]:
            
            text = page.extract_text()
            all_pages.append(text)
        return all_pages

if __name__ == "__main__":
    pages = extract_text(PDF_PATH)
    # pages = extract_text("../../data/DISCOM_TARIFF_ORDER_FY_2023-24.pdf")
    for i, p in enumerate(pages):
        print(f"--- Page {i+1} ---")
        print(p)
        print("\n\n")
