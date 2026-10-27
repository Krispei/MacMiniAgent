"""
    create_chunks.py

    This file recursively scans vault for all of the files and then chunks them according to my chunking strategy
"""

from pathlib import Path
from pypdf import PdfReader
import os
import json
from chunking_methods import chunk_by_tokens

FILES_PATH = Path('Test_docs')
CHUNKS_DB_PATH = Path('database/chunks')

def create_path(file):

    path = (CHUNKS_DB_PATH / file.relative_to(FILES_PATH)).with_suffix(".jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    return path

def chunk_pdf(files_pdf):
    pass


def chunk_md(files_md):

    for md in files_md:
        print(md)
        path = create_path(md)

        chunk_by_tokens(input=md, output=path)

def main():

    files_pdf = []
    files_md = []

    for p in FILES_PATH.rglob("*.pdf"):
        files_pdf.append(p)

    for p in FILES_PATH.rglob("*.md"):
        files_md.append(p)

    #chunk_pdf(files_pdf)
    chunk_md(files_md)

if __name__ == "__main__":
    main()