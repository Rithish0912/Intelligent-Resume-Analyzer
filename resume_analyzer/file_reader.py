import os
import zipfile
import xml.etree.ElementTree as ET

def read_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def read_docx_file(filepath):
    text_parts = []
    with zipfile.ZipFile(filepath, 'r') as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for t in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if t.text:
                    text_parts.append(t.text)
    return ' '.join(text_parts)

def read_resume(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.txt':
        return read_text_file(filepath)
    elif ext == '.docx':
        return read_docx_file(filepath)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Only .txt and .docx are allowed.")