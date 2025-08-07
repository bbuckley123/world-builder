from langgraph.graph import StateGraph, END
from langchain_ollama import OllamaLLM
from typing import TypedDict
from copy import deepcopy
import os
import yaml

from worldbuilder.prompt_loader import load_prompt
from worldbuilder.pipeline_loader import get_stable_diffusion_pipeline
from worldbuilder.paths import WORLD_YAML


# === TypedDicts ===

class City(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str

class Region(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str

class Continent(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str
    regions: list[Region]
    cities: list[City]

class Ocean(TypedDict):
    name: str
    description: str
    image_prompt: str
    image_path: str

class World(TypedDict):
    name: str
    genre: str
    description: str
    image_prompt: str
    image_path: str
    continents: list[Continent]
    oceans: list[Ocean]


# === I/O Helpers ===

def load_world_yaml() -> World:
    with open("world_with_descriptions.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_world_yaml(state: World, path: str = "world_with_images.yaml") -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(state, f, sort_keys=False, allow_unicode=True)
    print(f"✅ Saved image data to {path}")


# === Image Generation ===

def generate_image(prompt: str, output_path: str) -> str:
    dir_name = os.path.dirname(output_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    pipe = get_stable_diffusion_pipeline()
    result = pipe(
        prompt=prompt,
        negative_prompt="",
        num_inference_steps=40,
        guidance_scale=8.5,
        height=512,
        width=1024
    )

    result.images[0].save(output_path)
    return output_path

# === Prompt Generation Utility ===

def render_image_prompt(description: str, entity_type: str, name: str, llm: OllamaLLM) -> str:
    prompt = load_prompt("create_image_prompt.txt", {
        "description": description,
        "entity_type": entity_type,
        "name": name
    })
    return llm.invoke(prompt).strip()


# === Per-Entity Prompt + Image Nodes ===

def generate_world_image_prompt(state: World, llm: OllamaLLM) -> dict:
    print("generating world image prompt")
    prompt = render_image_prompt(state["description"], "world", state["name"], llm)
    return {"image_prompt": prompt}

def generate_world_image(state: World) -> dict:
    print("generating world image")
    path = "world_image.png"
    generate_image(state["image_prompt"], path)
    return {"image_path": path}


def generate_continent_images(state: World, llm: OllamaLLM) -> dict:
    print("generating continent images")
    updated = []
    for c in state["continents"]:
        prompt = render_image_prompt(c["description"], "continent", c["name"], llm)
        path = f"images/continents/{slugify(c['name'])}.png"
        generate_image(prompt, path)
        updated.append({**c, "image_prompt": prompt, "image_path": path})
    return {"continents": updated}


def generate_region_images(state: World, llm: OllamaLLM) -> dict:
    print("generating region images")
    updated_continents = []
    for continent in state["continents"]:
        updated_regions = []
        for r in continent.get("regions", []):
            prompt = render_image_prompt(r["description"], "region", r["name"], llm)
            path = f"images/regions/{slugify(r['name'])}.png"
            generate_image(prompt, path)
            updated_regions.append({**r, "image_prompt": prompt, "image_path": path})
        updated_continents.append({**continent, "regions": updated_regions})
    return {"continents": updated_continents}


def generate_city_images(state: World, llm: OllamaLLM) -> dict:
    print("generating city images")
    updated_continents = []
    for continent in state["continents"]:
        updated_cities = []
        for city in continent.get("cities", []):
            prompt = render_image_prompt(city["description"], "city", city["name"], llm)
            path = f"images/cities/{slugify(city['name'])}.png"
            generate_image(prompt, path)
            updated_cities.append({**city, "image_prompt": prompt, "image_path": path})
        updated_continents.append({**continent, "cities": updated_cities})
    return {"continents": updated_continents}


def generate_ocean_images(state: World, llm: OllamaLLM) -> dict:
    print("generating ocean images ")
    updated = []
    for ocean in state["oceans"]:
        prompt = render_image_prompt(ocean["description"], "ocean", ocean["name"], llm)
        path = f"images/oceans/{slugify(ocean['name'])}.png"
        generate_image(prompt, path)
        updated.append({**ocean, "image_prompt": prompt, "image_path": path})
    return {"oceans": updated}


# === Utility ===

def slugify(name: str) -> str:
    return name.lower().replace(" ", "_")


# === Finalization Step ===

def finalize_images(state: World) -> World:
    save_world_yaml(state, "world_with_images.yaml")
    return state


# === Build and Run ===

def build_and_run_image_graph(llm: OllamaLLM, state: World) -> None:
    def wrap(func):
        return lambda s: func(s, llm)

    builder = StateGraph(World)

    builder.add_node("generate_world_image_prompt", wrap(generate_world_image_prompt))
    builder.add_node("generate_world_image", generate_world_image)
    builder.add_node("generate_continent_images", wrap(generate_continent_images))
    builder.add_node("generate_region_images", wrap(generate_region_images))
    builder.add_node("generate_city_images", wrap(generate_city_images))
    builder.add_node("generate_ocean_images", wrap(generate_ocean_images))
    builder.add_node("finalize", finalize_images)

    builder.set_entry_point("generate_world_image_prompt")
    builder.add_edge("generate_world_image_prompt", "generate_world_image")
    builder.add_edge("generate_world_image", "generate_continent_images")
    builder.add_edge("generate_continent_images", "generate_region_images")
    builder.add_edge("generate_region_images", "generate_city_images")
    builder.add_edge("generate_city_images", "generate_ocean_images")
    builder.add_edge("generate_ocean_images", "finalize")
    builder.add_edge("finalize", END)

    graph = builder.compile()
    graph.invoke(deepcopy(state))


# === Main ===

def main():
    state = load_world_yaml()
    llm = OllamaLLM(model="llama3.1:8b-instruct-q8_0")
    build_and_run_image_graph(llm, state)

if __name__ == "__main__":
    main()
