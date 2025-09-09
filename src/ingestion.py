import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = []
    for page in doc:
        text_data.append(page.get_text("text"))
    return "\n".join(text_data)
