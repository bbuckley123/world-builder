import os
from smolagents import ToolCallingAgent, LiteLLMModel
from .utils import local_yaml_writer, load_prompt

SHOULD_VALIDATE = False

def create_continents(world_yaml: str, model: LiteLLMModel, max_retries: int = 3) -> str:
    """Generate continents.yaml based on world_yaml. Returns the YAML string."""
    continent_prompt = load_prompt("create_continents.txt").format(world_yaml=world_yaml)
    continent_agent = ToolCallingAgent(
        name="ContinentCreatorAgent",
        tools=[local_yaml_writer],
        model=model,
    )
    validating_agent = ToolCallingAgent(
        name="ContinentValidatingAgent",
        tools=[],
        model=model,
    )

    for attempt in range(max_retries):
        print(f"\n=== Attempt {attempt + 1} to generate continents.yaml ===")
        continent_agent.run(continent_prompt)

        if not os.path.exists("continents.yaml"):
            print("continents.yaml was not created. Retrying...")
            continue

        with open("continents.yaml", "r", encoding="utf-8") as f:
            continents_yaml = f.read()

        if SHOULD_VALIDATE == True:
            validate_prompt = load_prompt("validate_continents.txt").format(
                world_yaml=world_yaml,
                continents_yaml=continents_yaml,
            )

            validation_result = validating_agent.run(validate_prompt)
            print("\nValidation Response:", validation_result)

            if validation_result.strip().startswith("VALID:"):
                print("\n✅ Continents are valid.")
                return continents_yaml
            else:
                print("\n❌ Validation failed. Reason:")
                print(validation_result)

    raise RuntimeError("Failed to generate valid continents.yaml")
