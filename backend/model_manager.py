from ctransformers import AutoModelForCausalLM

class LocalTextGenerator:
    """
    Phase 1: Ensures responses are strictly based on stored personal data.
    AI will NOT generate additional information beyond what is retrieved.
    """

    def __init__(self, model_path: str):
        print(f"🔄 Loading GGUF model from: {model_path}")

        # Load the GGUF model but restrict full AI generation
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type="mistral",  # Ensure the correct model type
            context_length=2048
        )

    def generate_text(self, retrieved_text: str, query: str = "", max_length: int = 50, temperature: float = 0.7, top_p: float = 0.9):
        """
        Returns the retrieved stored information exactly as it is.
        Ensures responses are formatted correctly without hallucination.
        """

        if not retrieved_text.strip():
            return "I don't have data for that."

        # Properly format the response without hallucination
        return retrieved_text.strip()
