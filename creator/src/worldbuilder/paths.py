from pathlib import Path

# Project root is one level up from /src/worldbuilder
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "output"
EXPORT_DIR = PROJECT_ROOT / "worlds"
DATA_DIR = PROJECT_ROOT / "world_data"
PROMPTS_PATH = SRC_DIR / "worldbuilder" / "prompts"

# Common files
NAMES_RAW_YAML = OUTPUT_DIR / "world_with_names_raw.yaml"
NAMES_YAML = OUTPUT_DIR / "world_with_names.yaml"
DESCRIPTIONS_YAML = OUTPUT_DIR / "world_with_descriptions.yaml"
WORLD_YAML = OUTPUT_DIR / "world.yaml"
IMAGES_BASE_DIR = OUTPUT_DIR / "images"
CONTINENTS_YAML = DATA_DIR / "continents.yaml"
OCEANS_YAML = DATA_DIR / "oceans.yaml"
WORLD_IMG = DATA_DIR / "world.png"

# Subfolders
CONTINENT_IMG_DIR = DATA_DIR / "continents"
OCEAN_IMG_DIR = DATA_DIR / "oceans"

# Create directories if they do not exist
for directory in (
    OUTPUT_DIR,
    EXPORT_DIR,
    DATA_DIR,
    IMAGES_BASE_DIR,
    CONTINENT_IMG_DIR,
    OCEAN_IMG_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

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
