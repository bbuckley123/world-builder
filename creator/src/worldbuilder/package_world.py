import os
import yaml
import json
import shutil
import logging
from worldbuilder.paths import WORLD_YAML, IMAGES_BASE_DIR, EXPORT_DIR
logger = logging.getLogger(__name__)


def slugify(name: str) -> str:
    return name.lower().replace(" ", "_")

def package_current_world():
    # Load recently generated world
    with open(WORLD_YAML, "r", encoding="utf-8") as f:
        state = yaml.safe_load(f)

    world_id = slugify(state["name"])
    world_dir = EXPORT_DIR / world_id
    os.makedirs(world_dir, exist_ok=True)

    # Copy world.yaml
    packaged_yaml = world_dir / "world.yaml"
    shutil.copy(WORLD_YAML, packaged_yaml)

    image_dst_root = world_dir / "images"
    os.makedirs(image_dst_root, exist_ok=True)

    # Copy the world image
    generated_world_image = IMAGES_BASE_DIR / "world.png"
    if os.path.exists(generated_world_image):
        shutil.copy(generated_world_image, os.path.join(image_dst_root, "world.png"))

    # Copy all sub-image directories (continents, regions, cities, etc.)
    for folder in [IMAGES_BASE_DIR / "continents", IMAGES_BASE_DIR / "regions", IMAGES_BASE_DIR / "cities", IMAGES_BASE_DIR / "oceans"]:
        if os.path.exists(folder):
            shutil.copytree(folder, os.path.join(image_dst_root, os.path.basename(folder)), dirs_exist_ok=True)

    # Update worlds.json
    update_world_index(state, world_id)

def update_world_index(state, world_id):
    index_file = os.path.join(EXPORT_DIR, "worlds.json")
    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            worlds = json.load(f)
    else:
        worlds = []

    # Remove any existing entry for this world
    worlds = [w for w in worlds if w["id"] != world_id]

    worlds.append({
        "id": world_id,
        "name": state["name"],
        "genre": state.get("genre", ""),
        "description": state.get("description", ""),
        "preview": f"{world_id}/images/world.png"
    })

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(worlds, f, indent=2)

    logger.info("Updated worlds index at %s", index_file)

def main() -> None:
    package_current_world()

if __name__ == "__main__":
    main()
