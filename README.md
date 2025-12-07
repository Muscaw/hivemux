# HoneyComb

HoneyComb is a cli tool allowing easy management of your tmux environments.

What HoneyComb provides the following features:
- create pre-defined sessions based on projects found in your workspace
- join pre-started session if one already exists in your environment

## Installation

`pipx install honeycomb-cli`

## Configuration

HoneyComb can be configured through a TOML file in `$HOME/.config/honeycomb/config.toml`.

If you have `XDG_CONFIG_HOME` or `XDG_CONFIG_DIRS` set, HoneyComb will look in these locations as described in the [XDG specification](https://specifications.freedesktop.org/basedir/latest/#basics).

HoneyComb works well without a config file set, by default, it acts with the default values described below.

_config.toml_
```toml
# Path to your workspace containing all your projects
workspace_path = "~/workspace"

# Pattern to match to find all the projects in the first level of your workspace folder. Must match Python's Path.glob() definition https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
workspace_markers = ["*/.git"]

# Additional search paths to add to your list of projects. The list is taken as-is and added to the project list.
additional_search_paths = []

# .combrc file used to define how to create the session for all projects
combrc = """
  new-session -d -c {{cwd}} -s {{session}} -n source nvim .
  new-window -c {{cwd}} -t {{session}} -n shell
  select-window -t {{session}}:source
"""
```

### A note on combrc

HoneyComb creates TMUX sessions based on a template. By default, this template lives in the HoneyComb code unless overriden by the config.toml file.
This gives the ability to define a personal and custom session creator.

To override the default combrc, the config.toml file provides a field called `combrc` that will be used instead of the default combrc script provided by HoneyComb.

A combrc file can also be created per project. For example, if your project is under `$HOME/workspace/my_project`, you can override the global combrc file with a file `$HOME/workspace/my_project/.combrc`

The content of the combrc file is parsed through Jinja and therefore allows for some templating.

The following variables are passed to the template:
- session: name of the session
- cwd: absolute path of the project

After the rendering of the template is done, the content is passed directly to tmux without modifications.

The commands defined in the [TMUX documentation](https://man.openbsd.org/OpenBSD-current/man1/tmux.1) can all be used.

#### What must the combrc file contain

A combrc script **must** contain the following line at the beginning.

`new-session -d -c {{cwd}} -s {{session}}`

This allows tmux to create the session without attaching to it, allowing HoneyComb to finish its execution.

If you want, you can always add [other flags](https://man.openbsd.org/OpenBSD-current/man1/tmux.1#new-session) to the `new-session` command such as `-n` or even a shell command.


## Usage

`comb --help`

`comb list-projects`

`comb attach myproject` or `comb a myproject`

### Shell auto-completion

#### ZSH

In your .zshrc, add the following line.

```bash
eval "$(_COMB_COMPLETE=zsh_source comb)"
```

#### bash

In your .bashrc, add the following line.

```bash
eval "$(_COMB_COMPLETE=bash_source comb)"
```
