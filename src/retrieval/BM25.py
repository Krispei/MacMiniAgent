from rank_bm25 import BM25Okapi
import re

def tokenize(text: str) -> list[str]:
    '''tokenizes str, used for BM25 search

    Args:
        text: text to be tokenized
    
    Returns:
        List[str] where each item corresponds to one token
    '''

    # Currently case-insensitive and tokens include punctuation
    return text.lower().split()

class BM25Search:
    def __init__(self):
        self.docs = []
        self.index = None

    def build(self, docs):
        '''Builds the BM25 index
        
        Args:
            docs: list[dict] with dict having key "content" containing the document content
        '''
        self.docs = docs

        if not docs:
            self.docs = None
            return

        corpus = [tokenize(m["content"]) for m in docs]

        self.index = BM25Okapi(corpus)

    def search(self, query, top_k=5):
        if self.index is None:
            return []

        scores = self.index.get_scores(tokenize(query))

        indicies = sorted(range(len(scores)), key=lambda x: scores[x], reverse=True)

        return [self.docs[i] for i in indicies[:top_k] if scores[i] > 0]