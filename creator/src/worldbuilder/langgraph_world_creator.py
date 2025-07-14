from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict, Annotated
import yaml
import random
from worldbuilder.image_generator import generate_image
from worldbuilder.paths import WORLD_IMG, WORLD_YAML
from worldbuilder.prompt_loader import load_prompt
from worldbuilder.spacy_extractor import extract_world_name

class WorldState(TypedDict):
    name: Annotated[str, lambda a, b : b]
    genre: Annotated[str, lambda a, b : b]
    continent_names: Annotated[list[str], lambda a, b : b]
    ocean_names: Annotated[list[str], lambda a, b : b]
    description: Annotated[str, lambda a, b : b]
    image_prompt: Annotated[str, lambda a, b : b]

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
    return {**state, "genre": selected_genre}

def generate_continent_names(state: WorldState, llm: OllamaLLM) -> WorldState:
    prompt = load_prompt("generate_continent_names.txt", {"genre": state["genre"]})
    result = llm.invoke(prompt).strip()
    items: list[str] = [item.strip() for item in result.split(",")]
    return {**state, "continent_names": items}

def generate_ocean_names(state: WorldState, llm: OllamaLLM) -> WorldState:
    prompt = load_prompt("generate_ocean_names.txt", {"genre": state["genre"]})
    result = llm.invoke(prompt).strip()
    items: list[str] = [item.strip() for item in result.split(",")]
    return {**state, "ocean_names": items}

def wait_for_name_generation(state: WorldState) -> WorldState:
    return state

def wait_for_name_generation_router(state: WorldState) -> str:
    if state["continent_names"] and state["ocean_names"]:
        return "proceed"
    return "wait"

def generate_world_description(state: WorldState, llm: OllamaLLM) -> WorldState:
    input = {
        "genre": state["genre"],
        "ocean_names": state["ocean_names"],
        "continent_names": state["continent_names"]
    }
    prompt = load_prompt("create_world.txt", input)
    result = llm.invoke(prompt).strip()
    return {**state, "description": result}

def extract_world_name_from_state(state: WorldState) -> WorldState:
    description = state["description"]
    name = extract_world_name(description)
    return {**state, "name": name}

def generate_image_prompt(state: WorldState, llm: OllamaLLM) -> WorldState:
    result = llm.invoke(f"Create a prompt for a Stable Diffusion image generator to generate an image for a world with the following description <begin-description> '{state['description']}' <end-description>. You can be creative. You can describe the whole world, or describe a very interesting part of the world. But you have limitations. Do *not* communicate with the end user. *Only* generate a stable diffusion prompt and nothing more. You *must* stay under 50 words.")
    print("🔍 Raw image_prompt result:", result, type(result))
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
    builder.add_node("generate_continent_names", wrap(generate_continent_names))
    builder.add_node("generate_ocean_names", wrap(generate_ocean_names))
    # builder.add_node("wait_for_name_generation", wrap_state(wait_for_name_generation))
    builder.add_node("generate_world_description", wrap(generate_world_description))
    builder.add_node("extract_world_name_from_state", wrap_state(extract_world_name_from_state))
    builder.add_node("generate_image_prompt", wrap(generate_image_prompt))
    builder.add_node("generate_image_from_prompt", wrap(generate_image_from_prompt))
    builder.add_node("finalize", lambda state: (write_world_yaml(state), state)[1])

    builder.set_entry_point("generate_genre")

    builder.add_edge("generate_genre", "generate_continent_names")
    builder.add_edge("generate_genre", "generate_ocean_names")
    builder.add_edge("generate_continent_names", "generate_world_description")
    builder.add_edge("generate_ocean_names","generate_world_description")
    builder.add_edge("generate_world_description", "extract_world_name_from_state")
    builder.add_edge("extract_world_name_from_state", "generate_image_prompt")
    builder.add_edge("generate_image_prompt", "generate_image_from_prompt")
    builder.add_edge("generate_image_from_prompt", "finalize")
    builder.add_edge("finalize", END)

    graph = builder.compile()
    graph.invoke({
        "name": None,
        "genre": None,
        "continent_names": None,
        "ocean_names": None,
        "description": None,
        "image_prompt": None
    })
