from dataclasses import dataclass
from pathlib import Path

from honeycomb.model import HoneyCombProject, HoneyCombProjectName, HoneyCombWorkspace


@dataclass(frozen=True)
class Workspace:
  human_friendly_name: str
  path: Path


def list_workspaces(
  base_workspace_path: HoneyCombWorkspace, additional_search_paths: list[Path], workspace_markers: list[str]
) -> set[HoneyCombProject]:
  projects: set[HoneyCombProject] = set()
  for pattern in workspace_markers:
    for match in base_workspace_path.path.glob(pattern):
      parent_path = match.parent
      projects.add(
        HoneyCombProject(path=parent_path, human_friendly_name=HoneyCombProjectName(parent_path.name.lower()))
      )
  for search_path in additional_search_paths:
    projects.add(HoneyCombProject(path=search_path, human_friendly_name=HoneyCombProjectName(search_path.name.lower())))
  return projects
