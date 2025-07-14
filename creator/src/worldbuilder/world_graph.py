from langchain_ollama import OllamaLLM
from worldbuilder.langgraph_world_creator import build_and_run_graph

def main() -> None:
    model = OllamaLLM(model="llama3.1:8b-instruct-q8_0")
    build_and_run_graph(model)
