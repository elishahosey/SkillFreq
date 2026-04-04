import os
import pdfplumber
from docx import Document
from pathlib import Path
import yaml
import os

def load_yaml(file_path: str) -> dict:
    """
    Load YAML file into dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("YAML file must contain a dictionary at the top level")

    return data

def load_resume(file_path: str) -> str:
    """
    Load resume text from PDF or DOCX.
    Returns raw text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_path = file_path.lower()

    if file_path.endswith(".pdf"):
        return _load_pdf(file_path)
    elif file_path.endswith(".docx"):
        return _load_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")


def _load_pdf(file_path: str) -> str:

    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

    return "\n".join(text)


def _load_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = []

    for para in doc.paragraphs:
        if para.text:
            text.append(para.text)

    return "\n".join(text)


def load_resume_signal(signal_path: Path)->dict:
    return load_yaml(signal_path)


#extract signals from resume document (find which area the resume is strongest)
def extract_resume_signals(file_path: str):
    text = load_resume(file_path)
    config = load_yaml("configs/resume_signal.yml")

    matches = {}

    text = text.lower()

    for skill, data in config.items():
        for alias in data["aliases"]:
            if alias in text:
                matches.setdefault(skill, []).append(alias)

    for skill, hits in matches.items():
        print(f"{skill}: {len(hits)} match(es) -> {hits}")
    return matches
