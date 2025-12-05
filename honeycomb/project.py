from honeycomb.model import HoneyCombProject, HoneyCombSession
from honeycomb.tmux import activate_window, attach, new_session, new_window


def start_new_project(project: HoneyCombProject) -> HoneyCombSession:
  session_name = project.derive_session_name()
  new_session(cwd=project.path, session_name=session_name, window_name="source", command=["nvim", "."])
  new_window(session_name, "shell")
  activate_window(session_name, "source")
  return session_name
