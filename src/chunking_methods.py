'''
    chunking_methods

    TODO Document differnnt chunking methods used
'''
import json


# Chunk by token variables

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

def chunk_by_tokens(input, output):
    '''
    chunk_by_tokens chunks the input text so that each chunk is CHUNK_SIZE characters and shares CHUNK_OVERLAP characters on both sides.

    TODO Add error handling for when chunk overlap is big enough so that the loop never progresses -> infinite loop 
    
    '''
    with open(input, "r", encoding="utf-8") as f:
        raw_text = f.read()

    with open(output, "w", encoding="utf-8") as f:

        idx = 1
        
        while raw_text:

            chunk = raw_text[:min(len(raw_text), CHUNK_SIZE)]

            if len(raw_text) <= CHUNK_SIZE:
                raw_text = ""
            else:
                raw_text = raw_text[CHUNK_SIZE-CHUNK_OVERLAP:]

            f.write(json.dumps({"file": str(input), "chunk": idx, "content": chunk}) + "\n")

            idx += 1