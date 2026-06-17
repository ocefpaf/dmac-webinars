---
author: Filipe Fernandes
title: pixi workflows
subtitle: Reproducibility doesn't have to be hard
date: Mar 27, 2025
history: true
---

# pixi workflows

![](images/zelda_meme.jpg)

# Before we start

Why another package manager?

>- We have the system ones: brew, choco, apt, yum, zypper, etc
>- We have language specific ones: pip/uv, conan, cargo, npm, etc
>- We have some system and language agnostic options: conda, mamba, micromamba, spack, brew (kind of), nix (also kind of), etc

# Project first vs Environment package management

- Conda/Mamba and Pip/venv require explicitly named & located dependency environments
- Most language specific package managers are project centric
- Python has explored this space as well (Poetry, PDM, Rye, now UV)
- Package manager takes on more roles
  - Managing and recording direct & indirect dependencies
  - Launching Python in the correct environment
  - Running additional tasks in the correct environment(s)

# Just another toy?

![](images/another_toy.png)

Is pixi just another toy we are playing with for a few days and throwing into the basket?


# What is pixi?

>- Pixi installs conda **and** PyPI packages
>    - Does not require an existing Python environment to install (or to wreck)
>- For pixi, everything is a project/environment, no Matlab like kitchen-sink
>- Reproducibility, replicability, and portability are first class citzens in a pixi workflow
>- Wicked fast


# What is a pixi workflow?

>- Well, what is **your** workflow?

. . .

Say, you need to download data from a server, create some metrics, and publish them in a webpage. Let's do that!

# (safe and scripted) Demonstration

[What could go wrong](pixi-demo/pixi.toml.example) ?

PS: One can import conda environments with `pixi init --import ./environment.yml`

<!--
- pixi global install depfinder
- depfinder gliders_of_the_day.ipynb
- pixi add 
- pixi shell
- pixi add nbclassic
-->

# Review: pixi toml config
```toml
[project]
authors = ["Filipe Fernandes <ocefpaf@gmail.com>"]
channels = ["conda-forge"]
description = "Add a short description here"
name = "glideroftheday"
platforms = ["linux-64"]
version = "0.1.0"

[tasks]

[dependencies]
```

# Review: pixi add

- We can add/remove as we go, the env is re-solved and the lockfile refreshed.

# Review: pixi lockfile

- Ensure the exact same version, same package, is used when re-creating the environment.
- Can be configued to create cross-platform lock files

> Why are lock files important? And why should our package manager automatically make them?
>
> In addition to reproducability, solving an environment on addition of a dependency, rather than on install
> makes sure that if the addition of the dependency is going to fail, it will fail early. That way
> the one who is likely to be the most capabile (the one adding the dependency) is the person who has to solve
> the conflicts, rather than other collaborators.

# Review: pixi info & tree

`pixi info` - How does pixi understand your project (and system)

`pixi tree` - Direct vs indirect dependencies

# Review: [tasks] field


```toml
map = "jupyter nbconvert --to notebook --execute in.ipynb --output=out.ipynb"
```

If there isn't a named task it will fall back to running the shell command in the environment.

```sh
pixi run env

COMMAND_MODE=unix2003
CONDA_CHANGEPS1=false
CONDA_DEFAULT_ENV=3CRS
CONDA_PREFIX=/Users/akerney/GMRI/NERACOOS/NERACOOS_ERDDAP_K8S/datasets/Brown/3CRS/.pixi/envs/default
CONDA_SHLVL=0
EDITOR=/usr/bin/nano
PATH=/Users/akerney/GMRI/NERACOOS/NERACOOS_ERDDAP_K8S/datasets/Brown/3CRS/.pixi/envs/default/bin:/Users/akerney/micromamba/condabin:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Users/akerney/.cargo/bin:/Users/akerney/.local/bin:/Users/akerney/.local/bin:/Users/akerney/.pixi/bin
PIXI_ENVIRONMENT_NAME=default
PIXI_ENVIRONMENT_PLATFORMS=osx-arm64,linux-64,linux-aarch64
PIXI_EXE=/opt/homebrew/bin/pixi
PIXI_IN_SHELL=1
PIXI_PROJECT_MANIFEST=/Users/akerney/GMRI/NERACOOS/NERACOOS_ERDDAP_K8S/datasets/Brown/3CRS/pixi.toml
PIXI_PROJECT_NAME=3CRS
PIXI_PROJECT_ROOT=/Users/akerney/GMRI/NERACOOS/NERACOOS_ERDDAP_K8S/datasets/Brown/3CRS
PIXI_PROJECT_VERSION=0.1.0
PIXI_PROMPT=(3CRS) 
```

# Review: tasks as a makefile

```toml
serve = { cmd = "cd html && python3 -m http.server 8080", depends-on = ["map"] }
```

# Environments and features

- Pixi can manage multiple environments per project in addition to the default environment
- Environments are composed of features, which are smaller collections of direct dependencies and tasks
- Can be configured to always have the same dependencies as other environments, or able to be solved indpendently
- `--environment` or `-e` to select an environment other than default or if a task is ambiguous

```toml
[dependencies]
xarray = ">=2024.03.0"

[feature.py39.dependencies]
python = "~=3.9.0"
[feature.py310.dependencies]
python = "~=3.10.0"

[feature.test.dependencies]
pytest = "*"
[feature.test.tasks]
test = "pytest ."

[feature.docs.dependencies]
sphinx = "*"
[feature.docs.tasks]
docs = "make html"

[environments]
default = {solve-group = "prod"}
test = {features = ["test"], solve-group = "prod"}
docs = {features = ["docs"], no-default-feature = true}
py39 = ["test", "py39"]
py310 = ["test", "py310"]
```

# Using pixi for CI: Python packages, and GHA

![](images/mp-different.gif)

- [CI-packages](https://github.com/ioos/ciso/blob/main/.github/workflows/tests.yml)
- [CI-GHA](https://github.com/ocefpaf/glideroftheday/blob/main/.github/workflows/publish_map.yaml)

# Review: pixi global

Pipx but now for Conda

>- Installs packages in a global space
>- Good option for CLI tools

# Review: pixi as conda alternative

Calling "pixi shell" activates a conda-like environment in the current project.

_`pixi global` can also be creatively used to make system wide environments similar to named Conda environments._

# Some extra commands that we should know

>- `pixi list`
>- `pixi update`

# Please check the Docs

If you want to become a pixi guru, please read the docs!

[https://pixi.sh/latest/](https://pixi.sh/latest/)

# Don't need Conda packages? Shipping to PyPI?

Consider checking out UV.

- Very similar project centric PyPI package manager
- Pixi uses it under the hood for installing PyPI packages

# Questions?

![](images/stromatolites.png)
