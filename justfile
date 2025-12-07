test:
  uv run python -m pytest

list:
  uv run python -m hivemux list-projects

attach project:
  uv run python -m hivemux attach {{project}}

check:
  uv run ruff format --check
  uv run ruff check
  just test

fix:
  uv run ruff format
  uv run ruff check --fix
