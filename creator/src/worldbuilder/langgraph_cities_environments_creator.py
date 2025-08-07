from typing import TypedDict
from langchain_ollama import OllamaLLM
from worldbuilder.prompt_loader import load_prompt
import random

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

def generate_environment_description(state, llm):
    prompt = load_prompt("generate_environment.txt", {"description": state['world_description']})
    description = llm.invoke(prompt).strip()
    return ""

def generate_city_description():
    return ""

def generate_cities_and_environments(state: str, llm: OllamaLLM):
    for continent in state["continents"]:
        environment_number = random.randint(1, 3)
        for i in range(1, environment_number):
            environment_description = generate_environment_description()
        # generate cities (input: environments, continent) 