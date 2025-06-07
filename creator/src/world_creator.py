from smolagents import ToolCallingAgent, LiteLLMModel
from .utils import local_yaml_writer, load_prompt


def create_world(model: LiteLLMModel) -> str:
    """Generate world.yaml using the provided LLM model and return its contents."""
    world_prompt = load_prompt("create_world.txt")
    agent = ToolCallingAgent(
        name="WorldCreatorAgent",
        tools=[local_yaml_writer],
        model=model,
    )
    agent.run(world_prompt)
    with open("world.yaml", "r", encoding="utf-8") as f:
        return f.read()
