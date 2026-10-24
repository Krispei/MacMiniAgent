'''
    embed.py 
'''

import llm_backend
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

# TODO: get the texts from database, append metadata, etc. 


