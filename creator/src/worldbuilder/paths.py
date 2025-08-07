from pathlib import Path

# Project root is one level up from /src/worldbuilder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"
DATA_DIR = PROJECT_ROOT / "world_data"
PROMPTS_PATH = SRC_DIR / "prompts"

# Common files
WORLD_YAML = OUTPUT_DIR / "world.yaml"
CONTINENTS_YAML = DATA_DIR / "continents.yaml"
OCEANS_YAML = DATA_DIR / "oceans.yaml"
WORLD_IMG = DATA_DIR / "world.png"

# Subfolders
CONTINENT_IMG_DIR = DATA_DIR / "continents"
OCEAN_IMG_DIR = DATA_DIR / "oceans"

def sanitize_name(name: str) -> str:
    """Sanitize a name so it's safe to use as a filename."""
    return name.strip().replace(" ", "_").replace("/", "_")

def continent_image_path(name: str) -> Path:
    """Return the full path to a continent image file."""
    return CONTINENT_IMG_DIR / f"{sanitize_name(name)}.png"

def ocean_image_path(name: str) -> Path:
    """Return the full path to an ocean image file."""
    return OCEAN_IMG_DIR / f"{sanitize_name(name)}.png"

def prompt_file(name: str) -> Path:
    return PROMPTS_PATH / name
