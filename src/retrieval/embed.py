import json
import ollama
from pathlib import Path
import math
import numpy as np

EMBEDDING_MODEL = "qwen3-embedding:0.6b"
INPUT = "database/chunks/"
OUTPUT = "database/embeddings.jsonl"

TEXT_FIELD = "content"
BATCH_SIZE = 64

QUERY_INSTRUCTION_PROMPT = "Instruct: Retrieve relevant passages from technical documents that answer the user's question. Query: "

def embed_documents():

    input_path = Path(INPUT)

    with open(OUTPUT, "w", encoding="utf-8") as out:

        for file in input_path.rglob("*.jsonl"):

            with open(file, "r", encoding="utf-8") as f:
                records = [json.loads(line) for line in f if line.strip()]

            texts = [f"{record["file"]} {record["content"]}" for record in records]

            resp = ollama.embed(model=EMBEDDING_MODEL, input=texts)

            for record, vec in zip(records, resp["embeddings"]):
                record["embedding"] = vec
                out.write(json.dumps(record) + "\n")

def get_document_embeddings():
    '''Returns chunk filepath, chunk contents, and embeddings for all chunks in DB
    
    Args:
        None

    Returns:
        sources: filepaths of each chunk
        chunks: chunk contents
        embeddings: embeddings of each chunk
    
    '''
    with open(OUTPUT, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]

    sources = []
    chunks = []
    embeddings = []

    for item in items:
        sources.append(item["file"])
        chunks.append(item["content"])
        embeddings.append(item["embedding"])

    sources = np.array(sources)
    chunks = np.array(chunks)
    embeddings = np.array(embeddings)

    return sources, chunks, embeddings

def embed_query(query):

    full_query = QUERY_INSTRUCTION_PROMPT + query

    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=full_query, keep_alive="10m")['embeddings']

    return np.array(query_embedding)


def main():
    embed_documents()

if __name__ == "__main__":
    main()



