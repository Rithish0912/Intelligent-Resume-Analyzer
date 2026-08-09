import math
import re
from collections import Counter
from stopwords import STOPWORDS

class TextPreprocessor:
    @staticmethod
    def tokenize(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = text.split()
        tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
        return tokens

class Document:
    def __init__(self, content, doc_id):
        self.doc_id = doc_id
        self.tokens = TextPreprocessor.tokenize(content)
        self.term_freq = Counter(self.tokens)
        self.vector = {}

class Corpus:
    def __init__(self, documents):
        self.documents = documents
        self.total_docs = len(documents)
        self.idf = {}
        self._compute_idf()

    def _compute_idf(self):
        doc_freq = Counter()
        for doc in self.documents:
            unique_terms = set(doc.term_freq.keys())
            doc_freq.update(unique_terms)
        for term, freq in doc_freq.items():
            self.idf[term] = math.log(self.total_docs / freq)

    def build_vectors(self):
        for doc in self.documents:
            vec = {}
            for term, tf in doc.term_freq.items():
                if term in self.idf:
                    vec[term] = tf * self.idf[term]
            doc.vector = vec

    def cosine_similarity(self, vec1, vec2):
        if not vec1 or not vec2:
            return 0.0
        common = set(vec1.keys()) & set(vec2.keys())
        dot = sum(vec1[t] * vec2[t] for t in common)
        norm1 = math.sqrt(sum(v*v for v in vec1.values()))
        norm2 = math.sqrt(sum(v*v for v in vec2.values()))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

def analyze_resumes(jd_content, resumes_contents):
    documents = []
    jd_doc = Document(jd_content, doc_id="JD")
    documents.append(jd_doc)
    for fname, content in resumes_contents.items():
        documents.append(Document(content, doc_id=fname))

    corpus = Corpus(documents)
    corpus.build_vectors()

    jd_vector = jd_doc.vector
    results = []
    for doc in documents[1:]:
        sim = corpus.cosine_similarity(jd_vector, doc.vector)
        results.append((doc.doc_id, sim))

    results.sort(key=lambda x: x[1], reverse=True)
    return results