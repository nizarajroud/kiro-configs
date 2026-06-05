"""Extract plain text from .docx files (ZIP containing XML)."""
import sys, zipfile, re

def extract_text(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    # Extract text between <w:t> tags
    texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', xml)
    # Join and split on paragraph markers for readability
    full = "".join(texts)
    # Re-extract with paragraph awareness
    paras = re.split(r'</w:p>', xml)
    result = []
    for p in paras:
        t = "".join(re.findall(r'<w:t[^>]*>([^<]+)</w:t>', p))
        if t.strip():
            result.append(t)
    return "\n".join(result)

if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(f"=== {f} ===")
        print(extract_text(f))
