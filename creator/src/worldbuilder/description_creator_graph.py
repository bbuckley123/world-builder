from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict
import yaml
import logging
from worldbuilder.paths import NAMES_YAML, DESCRIPTIONS_YAML
from worldbuilder.prompt_loader import load_prompt
from copy import deepcopy
logger = logging.getLogger(__name__)


# === TypedDict Definitions ===

class City(TypedDict):
    name: str
    description: str

class Region(TypedDict):
    name: str
    description: str

class Continent(TypedDict):
    name: str
    description: str
    regions: list[Region]
    cities: list[City]

class Ocean(TypedDict):
    name: str
    description: str

class World(TypedDict):
    name: str
    genre: str
    description: str
    continents: list[Continent]
    oceans: list[Ocean]


# === Load / Save YAML ===

def load_world_yaml() -> World:
    with open(NAMES_YAML, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_world_yaml(state: World) -> None:
    with open(DESCRIPTIONS_YAML, "w", encoding="utf-8") as f:
        yaml.dump(state, f, sort_keys=False, allow_unicode=True)
    logger.info("Saved updated world with descriptions to %s", DESCRIPTIONS_YAML)


# === Description Generators ===

def describe_world(state: World, llm: OllamaLLM) -> dict:
    logger.info("Describing the world")
    prompt = load_prompt("describe_world.txt", {
        "name": state["name"],
        "genre": state["genre"]
    })
    return {"description": llm.invoke(prompt).strip()}


def describe_continents(state: World, llm: OllamaLLM) -> dict:
    logger.info("Describing the continents")
    updated = []
    for c in state["continents"]:
        prompt = load_prompt("describe_continent.txt", {
            "name": c["name"],
            "genre": state["genre"]
        })
        updated.append({**c, "description": llm.invoke(prompt).strip()})
    return {"continents": updated}


def describe_oceans(state: World, llm: OllamaLLM) -> dict:
    logger.info("Describing the oceans")
    updated = []
    for o in state["oceans"]:
        prompt = load_prompt("describe_ocean.txt", {
            "name": o["name"],
            "genre": state["genre"]
        })
        updated.append({**o, "description": llm.invoke(prompt).strip()})
    return {"oceans": updated}


def describe_regions(state: World, llm: OllamaLLM) -> dict:
    logger.info("Describing the regions")
    updated_continents = []
    for continent in state["continents"]:
        updated_regions = []
        for r in continent.get("regions", []):
            prompt = load_prompt("describe_region.txt", {
                "name": r["name"],
                "continent": continent["name"],
                "genre": state["genre"]
            })
            updated_regions.append({**r, "description": llm.invoke(prompt).strip()})
        updated_continents.append({**continent, "regions": updated_regions})
    return {"continents": updated_continents}


def describe_cities(state: World, llm: OllamaLLM) -> dict:
    logger.info("Describing the cities")
    updated_continents = []
    for continent in state["continents"]:
        updated_cities = []
        for city in continent.get("cities", []):
            prompt = load_prompt("describe_city.txt", {
                "name": city["name"],
                "continent": continent["name"],
                "genre": state["genre"]
            })
            updated_cities.append({**city, "description": llm.invoke(prompt).strip()})
        updated_continents.append({**continent, "cities": updated_cities})
    return {"continents": updated_continents}


# === Finalization Step ===

def finalize_descriptions(state: World) -> World:
    logger.info("Finalizing description")
    save_world_yaml(state)
    return state


# === Build and Run Graph ===

def build_and_run_description_graph(llm: OllamaLLM, state: World) -> None:
    def wrap(func):
        return lambda s: func(s, llm)

    builder = StateGraph(World)

    builder.add_node("describe_world", wrap(describe_world))
    builder.add_node("describe_continents", wrap(describe_continents))
    builder.add_node("describe_oceans", wrap(describe_oceans))
    builder.add_node("describe_regions", wrap(describe_regions))
    builder.add_node("describe_cities", wrap(describe_cities))
    builder.add_node("finalize", finalize_descriptions)

    builder.set_entry_point("describe_world")
    builder.add_edge("describe_world", "describe_continents")
    builder.add_edge("describe_continents", "describe_oceans")
    builder.add_edge("describe_oceans", "describe_regions")
    builder.add_edge("describe_regions", "describe_cities")
    builder.add_edge("describe_cities", "finalize")
    builder.add_edge("finalize", END)

    graph = builder.compile()
    graph.invoke(deepcopy(state))


# === Main Entry ===

def main():
    state = load_world_yaml()

    llm = OllamaLLM(model="llama3.1:8b-instruct-q8_0")
    build_and_run_description_graph(llm, state)

if __name__ == "__main__":
    main()

