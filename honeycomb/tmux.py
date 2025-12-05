import os
import subprocess
from pathlib import Path

from honeycomb.model import HoneyCombSession, HoneyCombSessions


def new_session(cwd: Path, session_name: HoneyCombSession, window_name: str, command: list[str] | None = None) -> None:
  session_cmd = " ".join(command) if command is not None else ""
  _ = subprocess.run(
    [
      "tmux",
      "new-session",
      "-d",
      "-c",
      cwd.absolute(),
      "-s",
      session_name.to_tmux_session_name(),
      "-n",
      window_name,
      session_cmd,
    ],
  )


def new_window(session_name: HoneyCombSession, window_name: str) -> None:
  _ = subprocess.run(
    ["tmux", "new-window", "-t", session_name.to_tmux_session_name(), "-n", window_name],
  )


def has_session(session_name: HoneyCombSession) -> bool:
  res = subprocess.run(["tmux", "has-session", "-t", session_name.to_tmux_session_name()])
  return res.returncode == 0


def activate_window(session_name: HoneyCombSession, window_name: str) -> None:
  _ = subprocess.run(
    ["tmux", "select-window", "-t", f"{session_name.to_tmux_session_name()}:{window_name}"],
  )


def list_sessions() -> HoneyCombSessions:
  res = subprocess.run(
    ["tmux", "list-sessions", "-F", "'#{session_name}'"],
    text=True,
    capture_output=True,
  )
  res.check_returncode()
  sessions = [x.removeprefix("'").removesuffix("'") for x in res.stdout.splitlines()]
  return HoneyCombSessions(
    [HoneyCombSession.from_session_name(x) for x in sessions if HoneyCombSession.is_honeycomb_session(x)]
  )


def switch_client(session_name: HoneyCombSession) -> None:
  os.execvp("tmux", ["tmux", "switch-client", "-t", session_name.to_tmux_session_name()])


def attach(session_name: HoneyCombSession) -> None:
  os.execvp("tmux", ["tmux", "attach", "-t", session_name.to_tmux_session_name()])
