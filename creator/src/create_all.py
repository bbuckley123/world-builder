from smolagents import LiteLLMModel
from .world_creator import create_world
from .continent_creator import create_continents

OLLAMA_BASE = "http://host.docker.internal:11434"


def main() -> None:
    model = LiteLLMModel(model_id="ollama_chat/llama3.1:latest", api_base=OLLAMA_BASE)
    world_yaml = create_world(model)
    create_continents(world_yaml, model)


if __name__ == "__main__":
    main()
