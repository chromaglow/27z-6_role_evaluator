import json
from pathlib import Path
import pdfplumber

def extract_pages(pdf_path: Path):
    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append({"page": i + 1, "text": text})
    return pages

def main():
    pdf_path = Path("data/raw/layoff2.pdf")
    out_path = Path("data/extracted/layoff2_pages.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pages = extract_pages(pdf_path)
    out_path.write_text(json.dumps(pages, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} ({len(pages)} pages)")

if __name__ == "__main__":
    main()
