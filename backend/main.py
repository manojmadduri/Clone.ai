# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from db_manager import init_db, add_personal_text
from retrieval import embeddings_manager
from model_manager import LocalTextGenerator
from schemas import PersonalTextInput, QueryInput

# ✅ Enable debug-level logging to see any backend errors
logging.basicConfig(level=logging.DEBUG)

# ✅ Path to your local Mistral GGUF model
MODEL_PATH = "models/mistral-gguf/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
text_generator = LocalTextGenerator(model_path=MODEL_PATH)

# ✅ Initialize FastAPI app
app = FastAPI(
    title="Clone.AI Backend",
    description="A Local AI Assistant (Phase 1: Text Only)",
    version="1.0"
)

# ✅ Enable CORS for requests from your React frontend at http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """
    Root endpoint to confirm the backend is running.
    """
    return {"message": "Welcome to Clone.AI Backend 🚀"}

@app.post("/add_text")
def add_text(item: PersonalTextInput):
    """
    Endpoint to add new personal data (title + content).
    Immediately updates the FAISS index so the AI can recall the data.
    """
    try:
        added = add_personal_text(item.title, item.content)
        # If successfully added to DB, rebuild FAISS index
        if added:
            embeddings_manager.update_index()
            return {"status": "success", "message": "Text added and FAISS index updated."}
        else:
            return {"status": "duplicate", "message": "Title already exists in DB."}
    except Exception as e:
        logging.error(f"Error in add_text: {e}")
        return {"error": str(e)}

@app.post("/query_ai")
def query_ai(query: QueryInput):
    """
    Endpoint to query the AI using stored personal data.
    1) We refine the user query with spaCy (optional).
    2) We retrieve the top-1 relevant snippet from FAISS.
    3) We feed that snippet to the text generator (Phase 1 is minimal).
    4) Return the strict snippet (no hallucinations).
    """
    try:
        # ✅ NLP to refine the query (Optional)
        refined_query = embeddings_manager.preprocess_query(query.query)

        # ✅ Retrieve best match from FAISS
        result_text = embeddings_manager.search(refined_query, top_k=1)

        # If no valid data
        if "don't have data" in result_text or "no data" in result_text:
            return {"answer": "I don't have data for that."}

        # ✅ For Phase 1, we simply pass the retrieved snippet to the local generator
        prompt = (
            f"User: {query.query}\n"
            f"AI (answer strictly using retrieved fact, nothing extra): {result_text}"
        )

        # We limit max_length to ensure short, factual responses
        answer = text_generator.generate_text(prompt, max_length=50)

        return {"answer": answer.strip()}
    except Exception as e:
        logging.error(f"Error in query_ai: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # ✅ Initialize database (creates tables if not exist)
    init_db()
    # ✅ Run FastAPI using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
