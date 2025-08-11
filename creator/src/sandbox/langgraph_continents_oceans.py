import yaml
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from src.sandbox.image_generator import generate_image
from worldbuilder.paths import continent_image_path, ocean_image_path, CONTINENTS_YAML, OCEANS_YAML
from worldbuilder.prompt_loader import load_prompt
from src.sandbox.spacy_extractor import extract_continent_and_ocean_names
from pathlib import Path

class Environment(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str

class City(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str

class Continent(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str
    environments: list[Environment]
    cities: list[City]

class Ocean(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str

class WorldDetailState(TypedDict):
    world_description: str
    continent_names: List[str]
    ocean_names: List[str]
    continents: List[Continent]
    oceans: List[Ocean]

def generate_continent_and_ocean_details(state: WorldDetailState, llm: OllamaLLM) -> WorldDetailState:
    continents = []
    oceans = []

    for name in state["continent_names"]:
        description_prompt = load_prompt("describe_continent.txt", {"description": state['world_description'], "name": name})
        description = llm.invoke(description_prompt).strip()
        image_prompt = load_prompt("create_image_prompt.txt", {"description": description, "entity": "continent"})
        image_generator_prompt = llm.invoke(image_prompt).strip()
        generate_image(image_generator_prompt, continent_image_path(name))

        continents.append({
            "name": name,
            "description": description,
            "image_prompt": image_generator_prompt,
            "image_path": str(continent_image_path(name)),
        })

    for name in state["ocean_names"]:
        description_prompt = load_prompt("describe_ocean.txt", {"description": state['world_description'], "name": name})
        description = llm.invoke(description_prompt).strip()
        image_prompt = load_prompt("create_image_prompt.txt", {"description": description, "entity": "ocean"})
        image_generator_prompt = llm.invoke(image_prompt).strip()
        generate_image(image_generator_prompt, ocean_image_path(name))

        oceans.append({
            "name": name,
            "description": description,
            "image_prompt": image_generator_prompt,
            "image_path": str(continent_image_path(name)),
        })

    return {
        **state,
        "continents": continents,
        "oceans": oceans,
    }

def save_outputs_to_yaml(state: WorldDetailState) -> WorldDetailState:
    continents_path = CONTINENTS_YAML
    oceans_path = OCEANS_YAML

    with continents_path.open("w", encoding="utf-8") as f:
        yaml.dump(state["continents"], f, sort_keys=False, allow_unicode=True)

    with oceans_path.open("w", encoding="utf-8") as f:
        yaml.dump(state["oceans"], f, sort_keys=False, allow_unicode=True)

    print(f"✅ Saved {continents_path}")
    print(f"✅ Saved {oceans_path}")

    return state

def build_world_detail_graph(llm: OllamaLLM):
    def wrap(func):
        return lambda state: func(state, llm)
    
    def wrap_state(func):
        return lambda state: func(state)

    builder = StateGraph(WorldDetailState)

    builder.add_node("generate_details", wrap(generate_continent_and_ocean_details))
    builder.add_node("save_outputs", save_outputs_to_yaml)

    builder.set_entry_point("generate_details")

    builder.add_edge("generate_details", "save_outputs")
    builder.add_edge("save_outputs", END)

    return builder.compile()


def run_continent_ocean_generation(llm: OllamaLLM, world_state):
    graph = build_world_detail_graph(llm)
    initial_state = {
        "world_description": world_state["description"],
        "continent_names": world_state["continent_names"],
        "ocean_names": world_state["ocean_names"],
        "continents": [],
        "oceans": [],
    }
    result = graph.invoke(initial_state)
    return result



