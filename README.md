# World Builder

World Builder provides an end-to-end workflow for procedurally generating fictional worlds and exploring them in a web UI. The **creator** package assembles names, descriptions, and images using large language models, and the **viewer** package renders the resulting data for browsing.

## Architecture
- **Creator** – Python pipeline built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Ollama](https://ollama.ai/). It generates YAML data and images, then packages a world into a folder under `creator/worlds`.
- **Viewer** – React + Vite application. The app in `viewer/world-viewer` reads packaged worlds from its `public/worlds` directory and presents an interactive interface for exploring continents, oceans, regions, and cities.

## Repository Structure
- `creator/` – world generation scripts (`run.sh`, `package_world.py`, etc.), prompt templates, and output directories.
- `viewer/` – front-end code. The React project lives in `viewer/world-viewer` along with its `public` assets.

## Quick Start
### Generate a world
```bash
cd creator
./setup.sh                         # create virtual environment and install deps
python -m spacy download en_core_web_sm
./run.sh                           # generate a world package in worlds/
```

### View generated worlds
```bash
cd viewer/world-viewer
npm install                        # install dependencies
# copy or symlink ../creator/worlds into public/worlds
npm run dev                        # start the Vite dev server
```
The viewer expects packaged worlds under `public/worlds`. After running the creator, copy the contents of `creator/worlds` there to explore them in the browser (default: http://localhost:5173).

## Makefile Commands
Common project tasks are exposed through the repository's `Makefile`:

```bash
make install                # install dependencies for creator and viewer
make lint                   # run linters for both projects
make lint PROJECT=viewer    # run linter for a single project
make test                   # run tests for both projects
make test PROJECT=creator   # run tests for a single project
make build                  # generate assets and build the viewer
make build PROJECT=viewer   # build only the viewer
```

`PROJECT` can be set to `creator` or `viewer` to scope a command.

## Project Goals
World Builder aims to make it easy to prototype imaginary worlds. The creator can be extended with new prompt pipelines or image generators, while the viewer renders the packaged data for users to explore.

## License
This project is licensed under the [MIT License](LICENSE).


