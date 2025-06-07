import os
from smolagents import ToolCallingAgent, LiteLLMModel, tool

# Optional prompt loader
def load_prompt(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

# === Tool definition ===
@tool
def local_file_writer(filename: str, content: str) -> str:
    """
    Write content to a local file on disk.
    
    Args:
        filename: The name of the file to write to, including extension.
        content: The string content to be written into the file.

    Returns:
        A confirmation message if successful, or an error message otherwise.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:
        return f"Failed to write file: {e}"

# === Setup model and agent ===
PROMPT_DIR = os.path.join(os.path.dirname(__file__), 'prompts')
prompt = load_prompt(os.path.join(PROMPT_DIR, 'create_world.txt'))

ollama_model = LiteLLMModel(
    model_id='ollama_chat/qwen2',
    api_base='http://host.docker.internal:11434'
)

agent = ToolCallingAgent(
    name="WorldCreatorAgent",
    tools=[local_file_writer],  # Your tool from above
    model=ollama_model
)

# === Run agent ===
agent.run(prompt)
