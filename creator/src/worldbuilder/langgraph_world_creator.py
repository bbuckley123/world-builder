from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict, Optional
import yaml
from pathlib import Path
from worldbuilder.image_generator import generate_image

# Define paths
DATA_DIR = Path(__file__).resolve().parent.parent / "world_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Define state
class WorldState(TypedDict):
    name: Optional[str]
    genre: Optional[str]
    description: Optional[str]
    image_prompt: Optional[str]

# Prompt steps
def generate_genre(state: WorldState, llm: OllamaLLM) -> WorldState:
    result = llm.invoke("Pick a genre like cyberpunk, steampunk, fantasy, or futuristic. This should be *ONE WORD*")
    return {**state, "genre": result.strip()}

def generate_name(state: WorldState, llm: OllamaLLM) -> WorldState:
    result = llm.invoke(f"Create a name for the world based on the genre: '{state['genre']}'. This should *ONLY* be a name. Do not generate any other content.")
    return {**state, "name": result.strip()}

def generate_description(state: WorldState, llm: OllamaLLM) -> WorldState:
    prompt = (
        f"Write a multi-paragraph narrative of a world in the '{state['genre']}' genre. The world's name is '{state['name']}' "
        f"The description must match the theme. Be vivid and creative. Describe the continents in the world, the oceans, the atmosphere, the climate, etc."
    )
    result = llm.invoke(prompt)
    return {**state, "description": result.strip()}

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

    output_path = generate_image(prompt)
    return {**state, "image_path": str(output_path)}

def write_world_yaml(state: WorldState) -> None:
    yaml_file = DATA_DIR / "world.yaml"
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

# Orchestrator
def build_and_run_graph(llm: OllamaLLM) -> None:
    def wrap(func):
        return lambda state: func(state, llm)

    builder = StateGraph(WorldState)
    builder.add_node("generate_genre", wrap(generate_genre))
    builder.add_node("generate_name", wrap(generate_name))
    builder.add_node("generate_description", wrap(generate_description))
    builder.add_node("generate_image_prompt", wrap(generate_image_prompt))
    builder.add_node("generate_image_from_prompt", wrap(generate_image_from_prompt))
    builder.add_node("finalize", lambda state: (write_world_yaml(state), state)[1])

    builder.set_entry_point("generate_genre")
    builder.add_edge("generate_genre", "generate_name")
    builder.add_edge("generate_name", "generate_description")
    builder.add_edge("generate_description", "generate_image_prompt")
    builder.add_edge("generate_image_prompt", "generate_image_from_prompt")
    builder.add_edge("generate_image_from_prompt", "finalize")
    builder.add_edge("finalize", END)

    graph = builder.compile()
    graph.invoke({"name": None, "genre": None, "description": None, "image_prompt": None})
