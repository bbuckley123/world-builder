from pathlib import Path
from smolagents import ToolCallingAgent, LiteLLMModel
from worldbuilder.utils import local_file_writer, load_prompt, DATA_DIR

WORLD_FILE = DATA_DIR / "world.yaml"

def create_world(model: LiteLLMModel) -> str:
    """Generate world.yaml using the provided LLM model and return its contents."""
    world_prompt = load_prompt("create_world_narrative.txt")
    agent = ToolCallingAgent(
        name="WorldCreatorAgent",
        tools=[local_file_writer],
        model=model,
    )
    agent.run(world_prompt)
