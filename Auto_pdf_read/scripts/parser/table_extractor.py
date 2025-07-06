import camelot
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "data", "DISCOM_TARIFF_ORDER_FY_2023-24.pdf")

# page 3 only
tables = camelot.read_pdf(PDF_PATH, pages="3", flavor="lattice")

print(f"Found {tables.n} tables")

for i, table in enumerate(tables):
    print(f"\n--- Table {i+1} ---\n")
    print(table.df)
