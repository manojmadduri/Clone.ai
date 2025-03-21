import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from db_manager import get_all_personal_texts
import spacy

# Load spaCy NLP model for query preprocessing
nlp = spacy.load("en_core_web_sm")

# FAISS Index Configuration
INDEX_FILE = "personal_faiss.index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class EmbeddingsManager:
    """
    Handles FAISS-based retrieval of personal data.
    """

    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.dimension = 384  # MiniLM embedding output size

        # Load or create FAISS index
        if os.path.exists(INDEX_FILE):
            print("✅ Loading existing FAISS index...")
            self.index = faiss.read_index(INDEX_FILE)
        else:
            print("⚡ No FAISS index found. Creating a new one...")
            self.index = faiss.IndexFlatL2(self.dimension)

        self.corpus = []
        self.text_map = {}  # Stores mapping from FAISS index to original text
        self.load_corpus_into_index()

    def load_corpus_into_index(self):
        """
        Rebuild FAISS index from DB, ensuring real-time memory updates.
        """
        print("🔄 Updating FAISS index from stored memories...")
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
        Refresh FAISS index whenever new data is added.
        """
        self.load_corpus_into_index()

    def preprocess_query(self, query: str) -> str:
        """
        Enhances query understanding via NLP techniques like lemmatization.
        """
        doc = nlp(query)
        keywords = [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN", "VERB")]

        # Return refined query if possible; else, return original
        return " ".join(keywords) if keywords else query

    def search(self, query: str, top_k: int = 1):
        """
        Searches FAISS for the most relevant response.
        Returns structured data instead of hallucinated answers.
        """
        refined_query = self.preprocess_query(query)
        query_emb = self.model.encode([refined_query], show_progress_bar=False)

        distances, indices = self.index.search(np.array(query_emb, dtype=np.float32), top_k)

        if top_k == 0 or len(self.text_map) == 0:
            return "I don't have data for that."

        results = []
        for idx in indices[0]:
            if idx < len(self.corpus):
                results.append(self.text_map[idx])

        return results[0] if results else "I don't have data for that."

# Initialize a single instance for global use
embeddings_manager = EmbeddingsManager()
