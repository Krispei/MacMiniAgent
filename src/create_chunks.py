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
    '''
    chunk_md takes a list of pdf file paths from vault, chunks each one according to a chunking strategy, and then saves all chunks of each doc inside a jsonl file with the doc's path

    args: files_pdf: a list of paths pointing to all pdfs in vault that need to be chunked

    returns: None
    '''

    for pdf in files_pdf:

        path = create_path(pdf)
        
        chunk_by_tokens(input=pdf, output=path)

        '''
        with open(path, "w", encoding='utf-8') as f:
            reader = PdfReader(pdf)
            for idx, page in enumerate(reader.pages):
                text = page.extract_text()
                f.write(json.dumps({"chunk": idx+1, "content": text}) + "\n")
        '''
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