# world-builder

### Hierarchy
World: the top node.
Continents
Region
Zone
Locality
Structure
Site

### How to run

Run the project from the ``creator`` directory with:

```bash
python run.py
```

uv doesn't handle spacy's models. Here is the manual step:
```
python -m spacy download en_core_web_sm
```

### `world_data` directory

The `world_data` folder holds static assets that describe the base geography of
your world. It should contain:

- `world.png` – a base map image
- `continents.yaml` – metadata and names for available continents
- `oceans.yaml` – metadata and names for oceans
- `continents/` – images for each continent (PNG files)
- `oceans/` – images for each ocean (PNG files)

If the directory is missing, it will be created automatically, but the project
requires the above files for full functionality.

