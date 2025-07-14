from smolagents import LiteLLMModel
from src.sandbox.world_creator import create_world

OLLAMA_BASE = "http://localhost:11434"

def main() -> None:
    model = LiteLLMModel(model_id="ollama_chat/llama3.1:8b-instruct-q8_0", api_base=OLLAMA_BASE)
    create_world(model)

if __name__ == "__main__":
    main()
