# Guidelines for AI Contributors

This project uses automated assistants to help develop both the Creator (Python) and the Viewer (JavaScript).

## Required setup
- Install project dependencies by running `make install`.

## Required checks
- **Lint** the code by running `make lint`.
- **Test** the code by running `make test`.
- If either command fails, **fix the issues and rerun** before committing.

## Adding code
- Write or update tests for any new feature or bug fix.
- Keep commits focused and ensure the worktree is clean before committing.

## Development tips
- Use `rg` (ripgrep) for code search instead of `grep -R` or `ls -R`.
- When dependencies are added, update the appropriate dependency files (e.g., `uv` or `npm` lock files).
- Update CI/CD configuration in `.github/` if new dependencies or other changes require it.
