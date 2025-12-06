# HoneyComb

HoneyComb is a cli tool allowing easy management of your tmux environments.

What HoneyComb provides:
- create pre-defined sessions based on projects found in your workspace
- join pre-started session if one already exists in your environment

## Installation

`pipx install honeycomb-cli`

## Configuration

HoneyComb can be configured through a TOML file in `$HOME/.config/honeycomb/config.toml`.

_config.toml_
```toml
# Path to your workspace containing all your projects
workspace_path: "~/workspace"
# Pattern to match to find all the projects in the first level of your workspace folder. Must match Python's Path.glob() definition https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
workspace_markers: ["*/.git"]
# Additional search paths to add to your list of projects. The list is taken as-is and added to the project list.
additional_search_paths: []
```

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
