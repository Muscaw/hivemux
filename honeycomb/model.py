from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import override

SESSION_PREFIX = "comb_"


def _cleanup_session_name(session_name: str) -> str:
  return session_name.replace(".", "_")


@dataclass(frozen=True)
class HoneyCombSession:
  session_name: str

  def to_tmux_session_name(self) -> str:
    return f"{SESSION_PREFIX}{self.session_name}"

  @staticmethod
  def is_honeycomb_session(possible_session_name: str) -> bool:
    return possible_session_name.startswith(SESSION_PREFIX)

  @staticmethod
  def get_honeycomb_session_name(possible_session_name: str) -> str:
    return f"{SESSION_PREFIX}{possible_session_name}"

  @staticmethod
  def from_path(path: Path) -> HoneyCombSession:
    return HoneyCombSession(_cleanup_session_name(path.name.lower()))

  @staticmethod
  def from_session_name(value: str) -> HoneyCombSession:
    if not HoneyCombSession.is_honeycomb_session(value):
      raise ValueError(f"Could not create HoneyCombSession with non HoneyComb session name {value}")
    return HoneyCombSession(value.lower())


class HoneyCombSessionsContainsNonHoneyCombSessions(Exception):
  pass


@dataclass(frozen=True)
class HoneyCombSessions:
  sessions: list[HoneyCombSession]

  def get_session_for_project(self, project: HoneyCombProject) -> HoneyCombSession | None:
    return next(
      iter([x for x in self.sessions if HoneyCombSession.get_honeycomb_session_name(project.human_friendly_name) == x]),
      None,
    )


class CouldNotListWorkspacesException(Exception):
  def __init__(self, path: Path, reason: str) -> None:
    super().__init__(f"Could not list workspaces for {path.absolute()} because {reason}")


@dataclass(frozen=True)
class HoneyCombWorkspace:
  path: Path

  def __post_init__(self) -> None:
    if not self.path.is_dir():
      raise CouldNotListWorkspacesException(self.path, "path is not a dir")


class ProjectIsNotDirectoryException(Exception):
  def __init__(self, path: Path) -> None:
    super().__init__(self, f"Project is not a directory {path}")


@dataclass(frozen=True)
class HoneyCombProjectName(str):
  value: str


@dataclass(frozen=True)
class HoneyCombProject:
  path: Path
  human_friendly_name: HoneyCombProjectName

  def __post_init__(self) -> None:
    if not self.path.is_dir():
      raise ProjectIsNotDirectoryException(self.path)

  def derive_session_name(self) -> HoneyCombSession:
    return HoneyCombSession.from_path(self.path)
