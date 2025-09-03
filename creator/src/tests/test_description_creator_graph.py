import sys
from pathlib import Path

# Ensure the src directory is on the path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import types

# Stub external dependencies not installed in the test environment
fake_ollama = types.ModuleType("langchain_ollama")
class DummyOllamaLLM:
    def __init__(self, *_, **__):
        pass
    def invoke(self, prompt: str):
        return ""
fake_ollama.OllamaLLM = DummyOllamaLLM
sys.modules.setdefault("langchain_ollama", fake_ollama)

fake_graph = types.ModuleType("langgraph.graph")
class DummyStateGraph:
    def __init__(self, *_, **__):
        pass
fake_graph.StateGraph = DummyStateGraph
fake_graph.END = object()
fake_langgraph = types.ModuleType("langgraph")
fake_langgraph.graph = fake_graph
sys.modules.setdefault("langgraph", fake_langgraph)
sys.modules.setdefault("langgraph.graph", fake_graph)

import yaml
from worldbuilder import description_creator_graph as dcg


def test_load_world_yaml(tmp_path, monkeypatch):
    data = {
        "name": "TestWorld",
        "genre": "Fantasy",
        "description": "",
        "continents": [],
        "oceans": []
    }
    yaml_path = tmp_path / "world_with_names.yaml"
    yaml_path.write_text(yaml.safe_dump(data), encoding="utf-8")
    monkeypatch.setattr(dcg, "NAMES_YAML", yaml_path)
    assert dcg.load_world_yaml() == data


def test_save_world_yaml(tmp_path, monkeypatch):
    data = {
        "name": "SaveWorld",
        "genre": "Sci-Fi",
        "description": "",
        "continents": [],
        "oceans": []
    }
    yaml_path = tmp_path / "world_with_descriptions.yaml"
    monkeypatch.setattr(dcg, "DESCRIPTIONS_YAML", yaml_path)
    dcg.save_world_yaml(data)
    loaded = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    assert loaded == data


def test_describe_world(monkeypatch):
    state = {"name": "Promptia", "genre": "Mystery"}
    calls = {}

    def fake_load_prompt(name, variables):
        calls["name"] = name
        calls["variables"] = variables
        return f"{variables['name']} in {variables['genre']}"

    class LLM:
        def __init__(self):
            self.prompts = []
        def invoke(self, prompt):
            self.prompts.append(prompt)
            return "A mysterious world"

    llm = LLM()
    monkeypatch.setattr(dcg, "load_prompt", fake_load_prompt)
    result = dcg.describe_world(state, llm)

    assert result == {"description": "A mysterious world"}
    assert calls == {
        "name": "describe_world.txt",
        "variables": state,
    }
    assert llm.prompts == ["Promptia in Mystery"]


def test_describe_continents(monkeypatch):
    state = {
        "name": "Continentia",
        "genre": "Adventure",
        "description": "",
        "continents": [{"name": "Alpha"}, {"name": "Beta"}],
        "oceans": []
    }
    prompts = []

    def fake_load_prompt(name, variables):
        prompts.append((name, variables))
        return f"describe {variables['name']}"

    class LLM:
        def __init__(self):
            self.calls = []
        def invoke(self, prompt):
            self.calls.append(prompt)
            return f"desc for {prompt}"

    llm = LLM()
    monkeypatch.setattr(dcg, "load_prompt", fake_load_prompt)
    result = dcg.describe_continents(state, llm)

    assert [c["description"] for c in result["continents"]] == [
        "desc for describe Alpha",
        "desc for describe Beta",
    ]
    assert prompts == [
        ("describe_continent.txt", {"name": "Alpha", "genre": "Adventure"}),
        ("describe_continent.txt", {"name": "Beta", "genre": "Adventure"}),
    ]
    assert llm.calls == [
        "describe Alpha",
        "describe Beta",
    ]
