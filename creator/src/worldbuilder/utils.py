import os
from pathlib import Path
import yaml
from smolagents import tool


@tool
def local_yaml_writer(filename: str, content: str) -> str:
    """Write YAML content to a local ``.yaml`` file on disk.

    Args:
        filename: Name of the file to write. Must end with ``.yaml``.
        content: Either a YAML string or a Python ``dict``/``list`` to serialise.

    Returns:
        A success or error message.
    """
    if not filename.endswith(".yaml"):
        return "Error: Filename must end with .yaml"
    try:
        if isinstance(content, (dict, list)):
            content = yaml.dump(content, sort_keys=False, allow_unicode=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filename}"
    except Exception as e:  # pragma: no cover - just a safeguard
        return f"Failed to write file: {e}"
    
@tool
def local_file_writer(filename: str, content: str) -> str:
    """Write any content to a local ``.txt`` file on disk.

    Args:
        filename: Name of the file to write. Must end with ``.txt``.
        content: English text.

    Returns:
        A success or error message.
    """

    if not filename.endswith(".txt"):
        return "Error: Filename must end with .txt"

    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / "data"

    # 3. Make sure it exists
    data_dir.mkdir(parents=True, exist_ok=True)

    # 4. Write the file
    file_path = data_dir / filename
    try:
        file_path.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Failed to write file: {e}"



PROMPT_DIR = Path(__file__).resolve().parent / "prompts"
# Directory where intermediate YAML files are stored
DATA_DIR = Path(__file__).resolve().parent.parent / "world_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_prompt(name: str) -> str:
    """Return the contents of a prompt file from the prompts directory."""
    path = PROMPT_DIR / name
    return path.read_text(encoding="utf-8")
