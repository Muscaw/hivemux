from dataclasses import dataclass

from jinja2 import Template

from hivemux.config import Config
from hivemux.model import HivemuxProject, HivemuxSession
from hivemux.tmux import activate_window, new_session, new_window, source_tmux_file


def __old_start_new_project(project: HivemuxProject) -> HivemuxSession:
  session_name = project.derive_session_name()
  new_session(cwd=project.path, session_name=session_name, window_name="source", command=["nvim", "."])
  new_window(session_name, "shell")
  activate_window(session_name, "source")
  return session_name


@dataclass(frozen=True)
class ProjectManager:
  config: Config

  def start_new_project(self, project: HivemuxProject) -> HivemuxSession:
    session_name = project.derive_session_name()
    possible_project_hmrc = project.path / ".hmrc"
    if possible_project_hmrc.exists():
      hmrc = possible_project_hmrc.read_text()
    else:
      hmrc = self.config.hmrc
    print(hmrc)
    template = Template(hmrc)
    rendered_rc = template.render(session=session_name.to_tmux_session_name(), cwd=str(project.path.absolute()))  # pyright: ignore[reportAny]
    source_tmux_file(rendered_rc)
    return session_name
