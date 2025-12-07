from dataclasses import dataclass

from jinja2 import Template

from honeycomb.config import Config
from honeycomb.model import HoneyCombProject, HoneyCombSession
from honeycomb.tmux import activate_window, new_session, new_window, source_tmux_file


def __old_start_new_project(project: HoneyCombProject) -> HoneyCombSession:
  session_name = project.derive_session_name()
  new_session(cwd=project.path, session_name=session_name, window_name="source", command=["nvim", "."])
  new_window(session_name, "shell")
  activate_window(session_name, "source")
  return session_name


@dataclass(frozen=True)
class ProjectManager:
  config: Config

  def start_new_project(self, project: HoneyCombProject) -> HoneyCombSession:
    session_name = project.derive_session_name()
    possible_project_combrc = project.path / ".combrc"
    if possible_project_combrc.exists():
      combrc = possible_project_combrc.read_text()
    else:
      combrc = self.config.combrc
    print(combrc)
    template = Template(combrc)
    rendered_rc = template.render(session=session_name.to_tmux_session_name(), cwd=str(project.path.absolute()))  # pyright: ignore[reportAny]
    source_tmux_file(rendered_rc)
    return session_name
