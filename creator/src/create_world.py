import os
import yaml
from smolagents import ToolCallingAgent, LiteLLMModel, tool

@tool
def local_yaml_writer(filename: str, content: str) -> str:
    """
    Write YAML content to a local .yaml file on disk.

    Args:
        filename: The name of the file to write to, including .yaml extension.
        content: YAML string content to be written.

    Returns:
        A message confirming success or error.
    """
    if not filename.endswith(".yaml"):
        return "Error: Filename must end with .yaml"
    try:
        if isinstance(content, (dict, list)):
            content = yaml.dump(content, sort_keys=False, allow_unicode=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Failed to write file: {e}"

# === Setup ===
PROMPT_DIR = os.path.join(os.path.dirname(__file__), 'prompts')
OLLAMA_BASE = "http://host.docker.internal:11434"
ollama_model = LiteLLMModel(
    model_id='ollama_chat/llama3.1:latest',
    api_base=OLLAMA_BASE
)

# === Create world.yaml ===
world_prompt = open(os.path.join(PROMPT_DIR, 'create_world.txt')).read()
world_agent = ToolCallingAgent(
    name="WorldCreatorAgent",
    tools=[local_yaml_writer],
    model=ollama_model
)
world_agent.run(world_prompt)

# === Load world.yaml ===
with open("world.yaml", "r", encoding="utf-8") as f:
    world_yaml = f.read()

# === Generate continents.yaml ===
continent_prompt = open(os.path.join(PROMPT_DIR, "create_continents.txt")).read().format(world_yaml=world_yaml)
continent_agent = ToolCallingAgent(
    name="ContinentCreatorAgent",
    tools=[local_yaml_writer],
    model=ollama_model
)

continent_validating_agent = ToolCallingAgent(
    name="ContinentValidatingAgent",
    tools=[],
    model=ollama_model
)

max_retries = 3
for attempt in range(max_retries):
    print(f"\n=== Attempt {attempt + 1} to generate continents.yaml ===")
    continent_agent.run(continent_prompt)

    if not os.path.exists("continents.yaml"):
        print("continents.yaml was not created. Retrying...")
        continue

    with open("continents.yaml", "r", encoding="utf-8") as f:
        continents_yaml = f.read()

    validate_prompt = open(os.path.join(PROMPT_DIR, "validate_continents.txt")).read().format(
        world_yaml=world_yaml,
        continents_yaml=continents_yaml,
    )

    validation_result = continent_validating_agent.run(validate_prompt)
    print("\nValidation Response:", validation_result)

    if validation_result.strip().startswith("VALID:"):
        print("\n✅ Continents are valid.")
        break
    else:
        print("\n❌ Validation failed. Reason:")
        print(validation_result)

else:
    print("\n❌ Failed to generate valid continents.yaml after 3 attempts.")
