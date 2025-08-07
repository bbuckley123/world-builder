from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict, Annotated
import yaml
import random
import operator
from pprint import pprint
from worldbuilder.image_generator import generate_image
from worldbuilder.paths import WORLD_IMG, WORLD_YAML
from worldbuilder.prompt_loader import load_prompt

class WorldState(TypedDict):
    name: Annotated[str, lambda a, b : b if not a else a]
    genre: Annotated[str, lambda a, b : b]
    continent_names: Annotated[list[str], lambda a, b : b if not a else a]
    ocean_names: Annotated[list[str], lambda a, b : b if not a else a]
    description: Annotated[str, lambda a, b : b if not a else a]
    image_prompt: Annotated[str, lambda a, b : b if not a else a]

# Prompt steps
def generate_genre(state: WorldState, llm: OllamaLLM) -> WorldState:
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
    print(f"The selected genre is: {selected_genre}")
    return {**state, "genre": selected_genre}

def generate_world_name(state: WorldState, llm: OllamaLLM) -> WorldState:
    prompt = load_prompt("generate_world_name.txt", {"genre": state["genre"]})
    result = llm.invoke(prompt).strip()
    print(f"generated world name: {result}")
    return {**state, "name": result}

def generate_continent_names(state: WorldState, llm: OllamaLLM) -> WorldState:
    prompt = load_prompt("generate_continent_names.txt", {"genre": state["genre"]})
    result = llm.invoke(prompt).strip()
    items: list[str] = [item.strip() for item in result.split(",")]
    print(f"generated continent names: {items}")
    return {**state, "continent_names": items}

def generate_ocean_names(state: WorldState, llm: OllamaLLM) -> WorldState:
    prompt = load_prompt("generate_ocean_names.txt", {"genre": state["genre"]})
    result = llm.invoke(prompt).strip()
    items: list[str] = [item.strip() for item in result.split(",")]
    print(f"generated ocean names: {items}")
    return {**state, "ocean_names": items}

def generate_world_description(state: WorldState, llm: OllamaLLM) -> WorldState:
    print("Beginning to generate world description. This is what the sate looks like")
    pprint(state)
    input = {
        "genre": state["genre"],
        "ocean_names": state["ocean_names"],
        "continent_names": state["continent_names"]
    }
    prompt = load_prompt("create_world.txt", input)
    result = llm.invoke(prompt).strip()
    return {**state, "description": result}

def generate_image_prompt(state: WorldState, llm: OllamaLLM) -> WorldState:
    result = llm.invoke(f"Create a prompt for a Stable Diffusion image generator to generate an image for a world with the following description <begin-description> '{state['description']}' <end-description>. You can be creative. You can describe the whole world, or describe a very interesting part of the world. But you have limitations. Do *not* communicate with the end user. *Only* generate a stable diffusion prompt and nothing more. You *must* stay under 50 words.")
    return {**state, "image_prompt": result.strip()}

def generate_image_from_prompt(state: WorldState, _) -> WorldState:
    prompt = state['image_prompt']
    if not prompt:
        raise ValueError("Missing image prompt in state.")
    if not isinstance(prompt, str):
        raise TypeError(f"Expected image_prompt to be str, got {type(prompt)}: {prompt}")
    generate_image(prompt, WORLD_IMG)
    return {**state, "image_path": str(WORLD_IMG)}

def write_world_yaml(state: WorldState) -> None:
    yaml_file = WORLD_YAML
    with open(yaml_file, "w", encoding="utf-8") as f:
        yaml.dump(
            {
                "name": state["name"],
                "genre": state["genre"],
                "description": state["description"],
                "continent_names": state["continent_names"],
                "ocean_names": state["ocean_names"],
                "image_prompt": state["image_prompt"]
            },
            f,
            sort_keys=False,
            allow_unicode=True
        )
    print(f"Saved world to {yaml_file}")

def build_and_run_graph(llm: OllamaLLM) -> None:
    def wrap(func):
        return lambda state: func(state, llm)
    
    def wrap_state(func):
        return lambda state: func(state)

    builder = StateGraph(WorldState)

    builder.add_node("generate_genre", wrap(generate_genre))
    builder.add_node("generate_world_name", wrap(generate_world_name))
    builder.add_node("generate_continent_names", wrap(generate_continent_names))
    builder.add_node("generate_ocean_names", wrap(generate_ocean_names))
    builder.add_node("generate_world_description", wrap(generate_world_description))
    builder.add_node("generate_image_prompt", wrap(generate_image_prompt))
    builder.add_node("generate_image_from_prompt", wrap(generate_image_from_prompt))
    builder.add_node("finalize", lambda state: (write_world_yaml(state), state)[1])

    builder.set_entry_point("generate_genre")

    builder.add_edge("generate_genre", "generate_continent_names")
    builder.add_edge("generate_genre", "generate_ocean_names")
    builder.add_edge("generate_genre", "generate_world_name")
    builder.add_edge("generate_continent_names", "generate_world_description")
    builder.add_edge("generate_ocean_names", "generate_world_description")
    builder.add_edge("generate_world_name", "generate_world_description")
    builder.add_edge("generate_world_description", "generate_image_prompt")
    builder.add_edge("generate_image_prompt", "generate_image_from_prompt")
    builder.add_edge("generate_image_from_prompt", "finalize")
    builder.add_edge("finalize", END)

    graph = builder.compile()
    graph.invoke({
        "name": None,
        "genre": None,
        "continent_names": [],
        "ocean_names": [],
        "description": None,
        "image_prompt": None
    })
