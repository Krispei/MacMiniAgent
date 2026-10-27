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

    """ NOTE: converts to numpy arrays, fill in documentation later"""

    with open(OUTPUT, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f if line.strip()]

    sources = []
    embeddings = []

    for item in items:
        sources.append(item["file"])
        embeddings.append(item["embedding"])

    sources = np.array(sources)
    embeddings = np.array(embeddings)

    return sources, embeddings


def embed_query(query):

    full_query = QUERY_INSTRUCTION_PROMPT + query

    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=full_query)['embeddings']

    return np.array(query_embedding)


def main():
    embed_query("Find a burger recipe.")

if __name__ == "__main__":
    main()



