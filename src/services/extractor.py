import PyPDF2
import docx

def extract_text_from_file(file_path: str) -> str:
    """Very basic extractor: supports .txt and .pdf (optional PyPDF2)."""
    if file_path.endswith(".txt") or file_path.endswith('.csv'):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif file_path.endswith(".pdf"):
        try:
            text = ""
            pdf = PyPDF2.PdfReader(file_path)
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
        except Exception:
            return ""

    # DOCX
    elif file_path.endswith(".docx"):
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception:
            return ""
        
    return ""