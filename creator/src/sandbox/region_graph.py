from langchain_ollama import OllamaLLM
from src.sandbox.langgraph_continents_oceans import run_continent_ocean_generation
from worldbuilder.paths import WORLD_YAML
import yaml
from pathlib import Path

def main() -> None:
    model = OllamaLLM(model="llama3.1:8b-instruct-q8_0")

    if not WORLD_YAML.exists():
        raise FileNotFoundError(f"Missing world.yaml at {WORLD_YAML}")

    world_data = yaml.safe_load(WORLD_YAML.read_text(encoding="utf-8"))
    run_continent_ocean_generation(model, world_data["description"])
