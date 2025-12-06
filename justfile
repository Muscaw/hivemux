test:
  uv run python -m pytest

list:
  uv run python -m honeycomb list-projects

attach project:
  uv run python -m honeycomb attach {{project}}
