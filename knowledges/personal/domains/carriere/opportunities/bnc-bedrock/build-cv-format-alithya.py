"""
build_cv.py
===========
Génère un CV Alithya V17 en injectant les nouvelles expériences (fichiers .md)
dans le CV V16 existant (.docx).

Styles Alithya du template V16:
    - NormalArial    → paragraphe normal (bold pour "Client : ...", "Projet interne ...")
    - Gras           → titres d'expérience (# 8 Gen AI Architect) + "Environnement techno :"
    - Puce1          → bullet points
    - Date alignée   → <w:tab/> avec tab stop right pos=9354

Numérotation : les nouvelles expériences continuent après la dernière existante (#7 → #8, #9, #10).
Les expériences existantes ne sont PAS renumérotées.

Usage:
    python build_cv.py
"""

import os, re, zipfile
from pathlib import Path

# ─── Config ──────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
EXP_DIR = ASSETS_DIR / "experiences"
OUTPUT_DIR = BASE_DIR / "output"
DROPBOX_DIR = Path("/mnt/c/Users/nizar/Dropbox/AAA_PRIVATE_LIFE/Job/NIZAR/CVs/CV_officiels-Format-Alithya")

CV_PREFIX = "Alithya - AJROUD Nizar - CV FR-v"

def find_latest_cv():
    """Find the highest version CV across assets/ and output/ directories."""
    candidates = []
    for d in [ASSETS_DIR, OUTPUT_DIR]:
        for f in d.glob(f"{CV_PREFIX}*.docx"):
            m = re.search(r'v(\d+)\.docx$', f.name)
            if m:
                candidates.append((int(m.group(1)), f))
    if not candidates:
        raise FileNotFoundError(f"No CV found matching '{CV_PREFIX}*.docx'")
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0]  # (version_number, path)



# ─── XML helpers ─────────────────────────────────────────────────────────────

def esc(t):
    return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def _sp(t):
    return ' xml:space="preserve"' if t and (t[0]==" " or t[-1]==" ") else ""

def run_xml(text, bold=False):
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return f'<w:r>{rpr}<w:t{_sp(text)}>{esc(text)}</w:t></w:r>'

def tab_xml():
    return '<w:r><w:tab/></w:r>'

# ─── Paragraph builders (matching Alithya CV styles) ─────────────────────────

_SPACING = '<w:spacing w:line="360" w:lineRule="auto"/>'
_TAB_RIGHT = '<w:tabs><w:tab w:val="right" w:pos="9354"/></w:tabs>'

def p_normal(text, bold=False):
    """NormalArial paragraph with 1.5 line spacing."""
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return f'<w:p><w:pPr><w:pStyle w:val="NormalArial"/>{_SPACING}{rpr}</w:pPr>{run_xml(text, bold=bold)}</w:p>'

def p_client_date(label, date):
    """Client/Projet line with date right-aligned via tab."""
    return (
        f'<w:p><w:pPr><w:pStyle w:val="NormalArial"/>{_TAB_RIGHT}{_SPACING}'
        f'<w:rPr><w:b/></w:rPr></w:pPr>'
        f'{run_xml(label, bold=True)}'
        f'<w:r><w:rPr><w:b/></w:rPr><w:tab/></w:r>'
        f'{run_xml(date, bold=True)}</w:p>'
    )

def p_gras_title(number, title):
    """Gras paragraph for experience title: # N [tab] Title."""
    return (
        f'<w:p><w:pPr><w:pStyle w:val="Gras"/></w:pPr>'
        f'{run_xml("# ", bold=False)}'
        f'{run_xml(str(number), bold=False)}'
        f'{tab_xml()}'
        f'{run_xml(title, bold=False)}</w:p>'
    )

def p_gras(text):
    """Gras paragraph (env techno header, etc.)."""
    return f'<w:p><w:pPr><w:pStyle w:val="Gras"/></w:pPr>{run_xml(text)}</w:p>'

def p_bullet(text):
    """Puce1 paragraph with 1.5 line spacing."""
    return f'<w:p><w:pPr><w:pStyle w:val="Puce1"/>{_SPACING}</w:pPr>{run_xml(text)}</w:p>'

def p_empty():
    """Empty NormalArial paragraph."""
    return '<w:p><w:pPr><w:pStyle w:val="NormalArial"/></w:pPr></w:p>'

# ─── Markdown → XML conversion ───────────────────────────────────────────────

def strip_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text

def md_to_xml(md_content):
    """Convert experience markdown to Word XML using Alithya styles."""
    lines = md_content.strip().splitlines()
    parts = []

    for line in lines:
        s = line.strip()
        if not s:
            parts.append(p_empty())
            continue

        # Blockquote → Client/Projet line with right-aligned date
        # Format: "> Client : Beneva (Assurance) 04/2026 à ce jour"
        # or: "> Projet interne · 03/2026 à 04/2026"
        if s.startswith("> "):
            text = s[2:].strip()
            # Try to split label from date (date pattern: MM/YYYY ...)
            m = re.match(r'^(.+?)\s+(\d{2}/\d{4}.*)$', text)
            if m:
                parts.append(p_client_date(m.group(1), m.group(2)))
            else:
                parts.append(p_normal(text, bold=True))

        # Experience title: # 10 AWS Cloud Architect → style Gras with tab
        elif s.startswith("# "):
            text = s[2:].strip()
            # Parse "10 AWS Cloud Architect" → number + title
            m_num = re.match(r'^(\d+)\s+(.+)$', text)
            if m_num:
                parts.append(p_gras_title(m_num.group(1), m_num.group(2)))
            else:
                parts.append(p_gras(text))

        # Bold line ending with ** (standalone bold paragraph)
        elif s.startswith("**") and s.endswith("**"):
            text = strip_md(s)
            parts.append(p_gras(text))

        # Bold prefix + rest: **Projet :** description or **Méthodologies :** ...
        elif s.startswith("**") and ":**" in s:
            text = strip_md(s)
            parts.append(p_normal(text, bold=True))

        # Bullet point
        elif s.startswith("* "):
            text = strip_md(s[2:])
            parts.append(p_bullet(text))

        # Sub-heading like "Environnement technologique :"
        elif s.endswith(":") and len(s) < 80:
            parts.append(p_gras(s))

        # Regular paragraph
        else:
            parts.append(p_normal(strip_md(s)))

    return "\n".join(parts)

# ─── Insertion logic ──────────────────────────────────────────────────────────

def find_insertion_point(xml):
    """Insert BEFORE the first existing experience 'Client : BENEVA 10/2024'."""
    beneva_idx = xml.find('>BENEVA<')
    if beneva_idx > 0:
        p_start = xml.rfind('<w:p ', 0, beneva_idx)
        if p_start < 0:
            p_start = xml.rfind('<w:p>', 0, beneva_idx)
        if p_start > 0:
            return p_start

    raise RuntimeError("Cannot find insertion point in document XML")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Auto-detect latest version
    current_version, template_path = find_latest_cv()
    next_version = current_version + 1
    output_path = OUTPUT_DIR / f"{CV_PREFIX}{next_version}.docx"

    exp_files = sorted(EXP_DIR.glob("*.md"))
    if not exp_files:
        print("❌  Aucun fichier .md trouvé dans experiences/")
        return

    print(f"📄  Template : {template_path.name} (v{current_version})")
    print(f"📦  {len(exp_files)} expériences à injecter :")
    for f in exp_files:
        print(f"    • {f.name}")
    print(f"🎯  Output : v{next_version}")

    # Convert each experience to XML
    new_experiences_xml = []
    for f in exp_files:
        md = f.read_text(encoding="utf-8")
        xml_content = md_to_xml(md)
        new_experiences_xml.append(xml_content)
        new_experiences_xml.append(p_empty())

    injected_xml = "\n".join(new_experiences_xml)

    # Read template docx
    with zipfile.ZipFile(template_path, "r") as z:
        doc_xml = z.read("word/document.xml").decode("utf-8")

    # Find insertion point and inject
    insert_pos = find_insertion_point(doc_xml)
    new_doc_xml = doc_xml[:insert_pos] + injected_xml + doc_xml[insert_pos:]

    # Write output docx
    if output_path.exists():
        output_path.unlink()

    with zipfile.ZipFile(template_path, "r") as zin, \
         zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = new_doc_xml.encode("utf-8")
            zout.writestr(item, data)

    print(f"\n✅  CV v{next_version} généré : {output_path}")

    # Copy to Dropbox
    if DROPBOX_DIR.exists():
        import shutil
        dropbox_copy = DROPBOX_DIR / output_path.name
        shutil.copy2(output_path, dropbox_copy)
        print(f"📁  Copié vers : {dropbox_copy}")
    else:
        print(f"⚠️  Dropbox introuvable : {DROPBOX_DIR}")

    print(f"    ⚠️  Ouvrir dans Word pour vérifier le formatage")

if __name__ == "__main__":
    main()
