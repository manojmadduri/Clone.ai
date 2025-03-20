import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from db_manager import get_all_personal_texts
import spacy

# Load spaCy for potential text-based query enhancements
nlp = spacy.load("en_core_web_sm")

INDEX_FILE = "personal_faiss.index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class EmbeddingsManager:
    """
    Builds and searches a FAISS index of personal data.
    """

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.dimension = 384  # Output dimension for all-MiniLM-L6-v2
        # Load or create FAISS index
        if os.path.exists(INDEX_FILE):
            print("✅ Loading existing FAISS index...")
            self.index = faiss.read_index(INDEX_FILE)
        else:
            print("⚡ No FAISS index found. Creating new index...")
            self.index = faiss.IndexFlatL2(self.dimension)

        self.corpus = []
        self.text_map = {}  # Map index -> original text
        self.load_corpus_into_index()

    def load_corpus_into_index(self):
        """
        Reset the FAISS index and add all existing data from the DB.
        """
        print("🔄 Rebuilding FAISS index from DB data...")
        self.index = faiss.IndexFlatL2(self.dimension)
        self.corpus.clear()
        self.text_map.clear()

        db_rows = get_all_personal_texts()
        embeddings = []

        for idx, (row_id, title, content) in enumerate(db_rows):
            text_data = f"{title} | {content}"
            self.corpus.append(text_data)
            self.text_map[idx] = text_data

            emb = self.model.encode([text_data], show_progress_bar=False)
            embeddings.append(emb[0])

        if embeddings:
            embeddings = np.array(embeddings, dtype=np.float32)
            self.index.add(embeddings)
            faiss.write_index(self.index, INDEX_FILE)

    def update_index(self):
        """
        Public method to refresh the index after inserting new data.
        """
        self.load_corpus_into_index()

    def preprocess_query(self, query: str) -> str:
        """
        Optional: refine the query to help FAISS retrieval (lemmatization, etc.).
        """
        doc = nlp(query)
        keywords = [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN", "VERB")]
        # If no keywords, use the original query
        return " ".join(keywords) if keywords else query

    def search(self, query: str, top_k: int = 1) -> str:
        """
        Search for the best matching data in FAISS, returns the top 1 snippet.
        """
        refined_query = self.preprocess_query(query)
        query_emb = self.model.encode([refined_query], show_progress_bar=False)

        distances, indices = self.index.search(np.array(query_emb, dtype=np.float32), top_k)

        if top_k == 0 or len(self.text_map) == 0:
            return "I have no data."

        best_idx = indices[0][0]
        if best_idx < len(self.corpus):
            return self.text_map[best_idx]
        else:
            return "I don't have data for that."

# Instantiate global manager
embeddings_manager = EmbeddingsManager()
