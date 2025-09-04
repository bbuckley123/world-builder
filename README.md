# World Builder

World Builder provides an end-to-end workflow for procedurally generating fictional worlds and exploring them in a web UI. The **creator** package assembles names, descriptions, and images using local large language models, and the **viewer** package serves that content for browsing.

## Architecture
- **Creator** – Python pipeline built with [LangGraph](https://github.com/langchain-ai/langgraph) and [Ollama](https://ollama.ai/). It generates YAML data and images, then packages a world into a folder under `creator/worlds`.
- **Viewer** – React + Vite application. The app in `viewer/world-viewer` reads packaged worlds from its `public/worlds` directory and presents an interactive interface for exploring continents, oceans, regions, and cities.

## Repository Structure
- `creator/` – world generation scripts (`run.sh`, `package_world.py`, etc.), prompt templates, and output directories.
- `viewer/` – front-end code. The React project lives in `viewer/world-viewer` along with its `public` assets.

## Quick Start
The creator builds worlds and the viewer serves them. This repository already contains a sample world and synced assets so you can explore immediately.

1. **Install dependencies**
   ```bash
   make install
   ```
2. **Launch the viewer**
   ```bash
   make dev
   ```
   Open <http://localhost:5173> to roam the prebuilt world.

To craft a fresh world on your machine:

```bash
make build PROJECT=creator   # run the creator pipeline
make sync-assets             # copy new worlds into the viewer
make dev                     # serve the viewer
```

See [creator/README.md](creator/README.md) for a detailed step-by-step guide to world generation.

## Makefile Commands
Common project tasks are exposed through the repository's `Makefile`:

```bash
make install                # install dependencies for creator and viewer
make install-viewer         # install viewer dependencies only
make install-creator        # install creator dependencies only
make lint                   # run linters for both projects
make lint-viewer            # lint the viewer only
make lint-creator           # lint the creator only
make test                   # run tests for both projects
make test-viewer            # test the viewer only
make test-creator           # test the creator only
make build                  # run creator, sync assets, and build viewer
make build-viewer           # build the viewer only
make build-creator          # run the creator pipeline only
make sync-assets            # copy creator/worlds into viewer/public/worlds
make dev                    # start the viewer dev server
make dev-viewer             # same as above; explicitly scopes to viewer
```

## Purpose
World Builder is a playground for seeing how much AI can run on modest hardware. Built on a MacBook Air, it operates entirely offline: a local LLM dreams up continents, oceans, cities, and even images for each one. You can kick off a run, walk away for a few hours, and return to a freshly imagined world. The creator can be extended with new prompt pipelines or image generators, while the viewer renders the packaged data for users to explore.

## License
This project is licensed under the [MIT License](LICENSE).


