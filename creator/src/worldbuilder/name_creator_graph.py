from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict
import yaml
import random
import logging
from pprint import pprint
from worldbuilder.paths import NAMES_RAW_YAML
from worldbuilder.prompt_loader import load_prompt
logger = logging.getLogger(__name__)

class City(TypedDict):
    name: str

class Region(TypedDict):
    name: str

class Continent(TypedDict):
    name: str
    regions: list[Region]
    cities: list[City]

class Ocean(TypedDict):
    name: str

class World(TypedDict):
    name: str
    genre: str
    continents: list[Continent]
    oceans: list[Ocean]

def empty_world() -> World:
    return {"name": "", "genre": "", "continents": [], "oceans": []}

def generate_entity_names(
    llm: OllamaLLM,
    prompt_file: str,
    template_replacements: dict,
) -> list[str]:
    prompt = load_prompt(prompt_file, template_replacements)
    result = llm.invoke(prompt).strip()
    return [item.strip() for item in result.split(",")]

def write_world_yaml(state: World) -> None:
    yaml_file = NAMES_RAW_YAML
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(
            state,
            f,
            sort_keys=False,
            allow_unicode=True
        )
    logger.info("Saved world to %s", yaml_file)

def generate_genre(state, llm) -> World:
    genres = [
        "High Fantasy",
        "Space Fantasy",
        "Steampunk",
        "Cyberpunk",
        "Superhero",
        "Futuristic",
    ]
    weights = [40, 20, 10, 10, 10, 10]

    selected_genre = random.choices(genres, weights=weights, k=1)[0]
    logger.info("The selected genre is: %s", selected_genre)
    return {**state, "genre": selected_genre}

def generate_world_name(state: World, llm: OllamaLLM):
    template_replacements = {"genre": state["genre"]}
    names = generate_entity_names(
        llm=llm,
        prompt_file="generate_world_name.txt",
        template_replacements=template_replacements
    )
    return {"name": names[0]}

def build_continents(names: list[str]) -> list[Continent]:
    return [{"name": name, "regions": [], "cities": []} for name in names]

def generate_continent_names(state, llm):
    template_replacements = {"genre": state["genre"]}
    names = generate_entity_names(
        llm=llm,
        prompt_file="generate_continent_names.txt", 
        template_replacements=template_replacements
    )
    return {"continents": build_continents(names)}

def build_oceans(names: list[str]) -> list[Ocean]:
    return [{"name": name} for name in names]

def generate_ocean_names(state, llm):
    template_replacements = {"genre": state["genre"]}
    names = generate_entity_names(
        llm=llm,
        prompt_file="generate_ocean_names.txt",
        template_replacements=template_replacements
    )
    return {"oceans": build_oceans(names)}

def build_regions(names: list[str]) -> list[Region]:
    return [{"name": name} for name in names]

def generate_region_names(state, llm):
    template_replacements = {"genre": state["genre"]}
    new_continents = []
    for continent in state["continents"]:
        names = generate_entity_names(
            llm=llm,
            prompt_file="generate_region_names.txt",
            template_replacements=template_replacements
        )
        regions = build_regions(names)
        new_continents.append({**continent, "regions": regions})
    return {"continents": new_continents}

def build_cities(names: list[str]) -> list[City]:
    return [{"name": name} for name in names]

def generate_city_names(state, llm):
    template_replacements = {"genre": state["genre"]}
    new_continents = []
    for continent in state["continents"]:
        names = generate_entity_names(
            llm=llm,
            prompt_file="generate_city_names.txt",
            template_replacements=template_replacements
        )
        cities = build_cities(names)
        new_continents.append({**continent, "cities": cities})
    return {"continents": new_continents}

def build_and_run_graph(llm: OllamaLLM) -> None:
    def wrap(func):
        return lambda state: func(state, llm)
    
    builder = StateGraph(World)

    builder.add_node("generate_genre", wrap(generate_genre))
    builder.add_node("generate_world_name", wrap(generate_world_name))
    builder.add_node("generate_continent_names", wrap(generate_continent_names))
    builder.add_node("generate_ocean_names", wrap(generate_ocean_names))
    builder.add_node("generate_region_names", wrap(generate_region_names))
    builder.add_node("generate_city_names", wrap(generate_city_names))
    builder.add_node("finalize", lambda state: (write_world_yaml(state), state)[1])

    builder.set_entry_point("generate_genre")
    builder.add_edge("generate_genre", "generate_world_name")
    builder.add_edge("generate_world_name", "generate_continent_names")
    builder.add_edge("generate_world_name", "generate_ocean_names")
    builder.add_edge("generate_continent_names", "generate_region_names")
    builder.add_edge("generate_region_names", "generate_city_names")
    builder.add_edge("generate_city_names", "finalize")
    builder.add_edge("finalize", END)

    graph = builder.compile()
    graph.invoke(empty_world())

def main() -> None:
    model = OllamaLLM(
        model="llama3.1:8b-instruct-q8_0",
    )
    build_and_run_graph(model)

if __name__ == "__main__":
    main()

