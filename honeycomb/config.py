from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Config:
  workspace_path: Path = Path.home() / "workspace"
  additional_search_paths: list[Path] = field(default_factory=lambda: [])
  workspace_markers: list[str] = field(default_factory=lambda: ["*/.git"])
  combrc: str = """new-session -d -c {{cwd}} -s {{session}} -n source nvim .
  new-window -c {{cwd}} -t {{session}} -n shell
  select-window -t {{session}}:source
  """

  @staticmethod
  def from_dict(data: dict[str, Any]) -> Config:  # pyright: ignore[reportExplicitAny]
    config_data = {}
    if "workspace_path" in data:
      config_data["workspace_path"] = Path(os.path.expanduser(data["workspace_path"]))  # pyright: ignore[reportAny]
    if "additional_search_paths" in data:
      config_data["additional_search_paths"] = [Path(os.path.expanduser(d)) for d in data["additional_search_paths"]]  # pyright: ignore[reportAny]
    if "workspace_markers" in data:
      config_data["workspace_markers"] = data["workspace_markers"]
    if "combrc" in data:
      config_data["combrc"] = data["combrc"]
    return Config(**config_data)  # pyright: ignore[reportUnknownArgumentType]


def get_config_possible_paths() -> list[Path]:
  possible_paths = [
    (
      Path.home() / ".config"
      if "XDG_CONFIG_HOME" not in os.environ
      else Path(os.path.expanduser(os.environ["XDG_CONFIG_HOME"]))
    )
  ]
  if "XDG_CONFIG_DIRS" in os.environ:
    possible_paths.extend([Path(os.path.expanduser(p)) for p in os.environ["XDG_CONFIG_DIRS"].split(":")])
  return possible_paths


def read_config() -> Config:
  possible_paths = get_config_possible_paths()
  for possible_path in possible_paths:
    config_path = possible_path / "honeycomb" / "config.toml"
    if not config_path.exists():
      continue
    with open(config_path, "rb") as file:
      read_config = tomllib.load(file)
      return Config.from_dict(read_config)
  # No match, so we return a default config file
  return Config()
