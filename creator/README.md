# Creator

The **creator** subproject assembles fully generated fantasy worlds entirely on your local machine.

## Prerequisites

- Install dependencies with [uv](https://github.com/astral-sh/uv).
- Install the small English SpaCy model:
  ```bash
  uv run python -m spacy download en_core_web_sm
  ```
- Local models: the default configuration expects LLaMA for text and Stable Diffusion for images, but you can swap in alternatives.

## Pipeline

Run each stage from this directory in order. Every command works inside the uv
environment and writes its intermediate results to the temporary `output/`
folder.

1. **Generate names**
   ```bash
   uv run namebuilder
   ```
   Produces `output/world_with_names_raw.yaml` containing a large list of
   candidate names.

2. **Trim the list**
   ```bash
   uv run name_chopper
   ```
   Reduces the raw list to a smaller set of entities and writes the result back
   to `output/`.

3. **Add descriptions**
   ```bash
   uv run descriptionbuilder
   ```
   Augments each entity with prose, creating `output/world_with_descriptions.yaml`.

4. **Generate images** *(resource intensive, may take a long time)*
   ```bash
   uv run imagebuilder
   ```
   Builds artwork for every item, yielding `output/world.yaml` and an accompanying
   `output/images/` directory.

5. **Package the world**
   ```bash
   uv run package_world
   ```
   Moves the finished world into the persistent `worlds/` directory and updates
   `worlds.json`, which indexes all generated worlds.

The `output/` directory is a throwaway workspace. Only the `worlds/` folder and
`worlds.json` are meant for long‑term storage.

## Testing

Run the project's tests with:

```bash
uv run python run_tests.py
```

## Notes

This project leans heavily on [LangGraph](https://github.com/langchain-ai/langgraph)
for orchestration. The pipeline is optimized so that even a MacBook Air can
produce a complete AI‑generated world with images, though the image generation
step can be lengthy. Feel free to substitute different models if your hardware
supports them.

