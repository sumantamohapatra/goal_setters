import pdfplumber
import camelot
import json
import os
from metadata_extractor import extract_metadata

def chunk_text(text, max_chunk_size=800):
    import re
    sentences = re.split(r'(?<=[.?!])\s+', text.strip())
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def process_pdf(pdf_path):
    chunks = []
    chunk_id = 0
    file_metadata = extract_metadata(pdf_path)
    print("✅ Detected metadata for chunking:", file_metadata)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                text_chunks = chunk_text(text)
                for t in text_chunks:
                    chunk_id += 1
                    chunks.append({
                        "chunk_id": f"chunk_{chunk_id}",
                        "chunk_type": "text",
                        "content": t,
                        "page_number": page_num,
                        "section_title": None,  # you could later add section detection
                        "metadata": file_metadata
                        
                    })
            # try to get tables on this page
            tables = camelot.read_pdf(pdf_path, pages=str(page_num), flavor="lattice")
            for table in tables:
                chunk_id += 1
                chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "chunk_type": "table",
                    "content": table.df.to_markdown(index=False),
                    "page_number": page_num,
                    "section_title": None,
                    "metadata": file_metadata
                    
                })
    return chunks

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    PDF_PATH = os.path.join(BASE_DIR, "data", "DISCOM_TARIFF_ORDER_FY_2023-24.pdf")
    result = process_pdf(PDF_PATH)
    with open(os.path.join(BASE_DIR, "data", "chunks.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(result)} chunks to chunks.json")
