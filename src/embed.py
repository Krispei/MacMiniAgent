import json
import ollama
from pathlib import Path
import math

EMBEDDING_MODEL = "qwen3-embedding:0.6b"
INPUT = "database/chunks/"
OUTPUT = "database/embeddings.jsonl"

TEXT_FIELD = "content"
BATCH_SIZE = 64


def embed_all():

    input_path = Path(INPUT)

    for file in input_path.rglob("*.jsonl"):

        with open(file, "r", encoding="utf-8") as f:
            records = [json.loads(line) for line in f if line.strip()]

        texts = [f"{record["file"]} {record["content"]}" for record in records]

        resp = ollama.embed(model=EMBEDDING_MODEL, input=texts)

        with open(OUTPUT, "w", encoding="utf-8") as out:

            for record, vec in zip(records, resp["embeddings"]):
                record["embedding"] = vec
                out.write(json.dumps(record) + "\n")

def main():

    embed_all()

if __name__ == "__main__":
    main()



