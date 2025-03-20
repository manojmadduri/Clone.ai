self.model = AutoModelForCausalLM.from_pretrained(
    model_path,
    local_files_only=True,
    torch_dtype=torch.float16,  # Use float16 for better GPU performance
    device_map="auto"  # Automatically uses GPU if available
)
