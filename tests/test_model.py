from pathlib import Path

import pytest

from honeycomb.model import HoneyCombProjectName, HoneyCombSession


class TestHoneyCombSession:
  @pytest.mark.parametrize(
    "session_name, tmux_session_name",
    [("a_name", "comb_a_name"), (".dot", "comb__dot"), ("a:project", "comb_a_project")],
  )
  def test_from_project_name_to_tmux_session_name(self, session_name: str, tmux_session_name: str) -> None:
    honeycomb_session = HoneyCombSession.from_project_name(HoneyCombProjectName(session_name))

    assert honeycomb_session.to_tmux_session_name() == tmux_session_name

  @pytest.mark.parametrize(
    "path, tmux_session_name",
    [
      ("/home/testuser/workspace/hello/", "comb_hello"),
      ("./workspace/.dot", "comb__dot"),
      ("/home/testuser/../othertestuser/:project", "comb__project"),
    ],
  )
  def test_from_path_to_tmux_session_name(self, path: str, tmux_session_name: str) -> None:
    honeycomb_session = HoneyCombSession.from_path(Path(path))

    assert honeycomb_session.to_tmux_session_name() == tmux_session_name

  @pytest.mark.parametrize(
    "session_name, tmux_session_name",
    [("comb__dot", "comb__dot"), ("comb_project_name", "comb_project_name")],
  )
  def test_from_session_name_to_tmux_session_name(self, session_name: str, tmux_session_name: str) -> None:
    honeycomb_session = HoneyCombSession.from_session_name(session_name)

    assert honeycomb_session.to_tmux_session_name() == tmux_session_name

  def test_from_session_fails_does_not_match_pattern(self) -> None:
    session_name_without_prefix = "hello"

    with pytest.raises(ValueError):
      _ = HoneyCombSession.from_session_name(session_name_without_prefix)
