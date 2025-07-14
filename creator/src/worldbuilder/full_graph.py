from langchain_ollama import OllamaLLM
from worldbuilder.langgraph_world_creator import build_and_run_graph
from worldbuilder.langgraph_continents_oceans import run_continent_ocean_generation
from worldbuilder.paths import WORLD_YAML
import yaml

def main() -> None:
    model = OllamaLLM(model="llama3.1:8b-instruct-q8_0")
    print("🌍 Running worldbuilder...")
    build_and_run_graph(model)

    if not WORLD_YAML.exists():
        raise FileNotFoundError(f"Missing world.yaml at {WORLD_YAML}")

    world_data = yaml.safe_load(WORLD_YAML.read_text(encoding="utf-8"))

    print("🗺️  Running continentsbuilder...")
    run_continent_ocean_generation(model, world_data["description"])
