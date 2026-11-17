import os
import glob
import zipfile
import xml.etree.ElementTree as ET
import re

def extract_text_from_docx(docx_path):
    """Standart zipfile orqali docx dan barcha matnlarni ajratib olish"""
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            # w:t teglari ichidagi barcha matnlarni yig'amiz
            texts = []
            for elem in tree.iter():
                if elem.tag.endswith('}t'):
                    if elem.text:
                        texts.append(elem.text)
                elif elem.tag.endswith('}p'):
                    texts.append('\n')
            return ''.join(texts)
    except Exception as e:
        return f"Xatolik docx: {e}"

def extract_text_from_doc(doc_path):
    """Oddiy .doc / rtf / binary stringlardan o'qiladigan matnlarni ajratish"""
    try:
        with open(doc_path, 'rb') as f:
            raw = f.read()
        # UTF-8 yoki CP1251 bo'yicha matn bo'laklarini qidirish
        # Word binary bo'lsa printable belgilarni olamiz
        text = raw.decode('utf-8', errors='ignore')
        # Agar rtf yoki html bo'lsa teglarini tozalaymiz
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\\[a-zA-Z0-9]+', ' ', clean)
        # O'zbekcha / ruscha harflar va bo'shliqlarni ajratamiz
        words = re.findall(r'[\w\d\.,:;\'"-]{3,}', clean)
        return ' '.join(words)
    except Exception as e:
        return f"Xatolik doc: {e}"

def extract_text_from_pdf(pdf_path):
    """pypdf orqali PDF matnini olish"""
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        pages_text = []
        for i, page in enumerate(reader.pages):
            t = page.extract_text()
            if t:
                pages_text.append(t)
        return '\n'.join(pages_text)
    except Exception as e:
        return f"Xatolik pdf: {e}"

def process_all_library_files():
    files = glob.glob("data/library/*.*")
    print(f"data/library dagi jami fayllar: {len(files)}")
    out_dir = "data/library_extracted"
    os.makedirs(out_dir, exist_ok=True)

    for f_path in files:
        base_name = os.path.basename(f_path)
        txt_out = os.path.join(out_dir, f"{os.path.splitext(base_name)[0]}.txt")
        ext = os.path.splitext(base_name)[1].lower()

        text = ""
        if ext == ".docx":
            text = extract_text_from_docx(f_path)
        elif ext == ".doc":
            text = extract_text_from_doc(f_path)
        elif ext == ".pdf":
            text = extract_text_from_pdf(f_path)

        if text and not text.startswith("Xatolik"):
            with open(txt_out, "w", encoding="utf-8") as out:
                out.write(text)
            print(f"[OK] {base_name} -> {len(text)} ta belgi matn ajratildi.")
        else:
            print(f"[!] {base_name}: {text[:100]}")

if __name__ == "__main__":
    process_all_library_files()

