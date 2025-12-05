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

  @staticmethod
  def from_dict(data: dict[str, Any]) -> Config:  # pyright: ignore[reportExplicitAny]
    config_data = {}
    if "workspace_path" in data:
      config_data["workspace_path"] = Path(os.path.expanduser(data["workspace_path"]))  # pyright: ignore[reportAny]
    if "additional_search_paths" in data:
      config_data["additional_search_paths"] = [Path(os.path.expanduser(d)) for d in data["additional_search_paths"]]  # pyright: ignore[reportAny]
    if "workspace_markers" in data:
      config_data["workspace_markers"] = data["workspace_markers"]
    return Config(**config_data)  # pyright: ignore[reportUnknownArgumentType]


def read_config() -> Config:
  config_path = Path.home() / ".config" / "honeycomb" / "config.toml"
  if not config_path.exists():
    return Config()
  with open(config_path, "rb") as file:
    read_config = tomllib.load(file)
    return Config.from_dict(read_config)
