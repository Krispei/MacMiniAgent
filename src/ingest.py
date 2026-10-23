"""
    ingest.py

    ingest.py scans the docs folder recursively, extracts text content from each 
    supported file (as well as the metadata), chunks the text
"""

from pathlib import Path
from pypdf import PdfReader
import os
import json

def main():

    file_dir = Path('docs')

    files = []

    for p in file_dir.rglob("*.pdf"):
        files.append(p)
    
    chunks_path = Path('database/chunks/')

    for file in files:

        path = (chunks_path / file.relative_to('docs')).with_suffix(".jsonl")

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding='utf-8') as f:
            reader = PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                f.write(json.dumps(text) + "\n")


if __name__ == "__main__":
    main()