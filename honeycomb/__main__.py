#!/usr/bin/env python3

from .cli import cli


def run_standard_action(session_name: str) -> None:
  if has_session(session_name):
    attach(session_name)
  else:
    new_session(session_name, "source", ["nvim", "."])
    new_window(session_name, "shell")
    activate_window(session_name, "source")
    attach(session_name)


def run_list_action() -> None:
  sessions = list_sessions()
  for session in sessions:
    print(session)


def run_list_possible_workspaces() -> list[str]:
  pass


if __name__ == "__main__":
  cli()
  #
  # args = parse_parameters(sys.argv)
  # session_name = args.session_name
  #
  # if session_name is None:
  #   session_name = os.path.basename(os.getcwd())
  #
  # if args.action_list:
  #   run_list_action()
  # else:
  #   session_name = cleanup_session_name(session_name)
  #   run_standard_action(session_name)


# if tmux has-session "$1"; then
#   tmux attach -t "$1"
# else
#   tmux new-session -d -s "$1" -n "source"
#   tmux new-window -t "$1" -d -n "shell"
# fi
