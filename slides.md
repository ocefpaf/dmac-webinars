---
author: Filipe Fernandes
title: pixi workflows
subtitle: Reproducibility doesn't have to be hard
date: Mar 27, 2025
history: true
---


# Before we start

Why another package manager?

>- We have the system ones: brew, choco, apt, yum, zypper, etc
>- We have language specific ones: pip/uv, cargo, npm, etc
>- We have some system and language agnostic options: conda, mamba, micromamba, brew (kind of), nix (also kind of), etc

. . . 

Is pixi just another toy we are playing with for a few days and throwing into the basket?


# What is pixi?

>- Pixi installs conda **and** PyPI packages
>- For pixi, everything is a project/environment, no Matlab like kitchen-sink
>- Reproducibility, replicability, and portability are first class citzens in a pixi workflow

# What is a pixi workflow?

>- Well, what is **your** workflow?

. . .

Say, you need to download data from a server, create some metrics, and publish them in a webpage. Let's do that!

# (safe and scripted) Demonstration

What could go wrong?


<!--
- pixi global install depfinder
- depfinder gliders_of_the_day.ipynb
- pixi add 
- pixi shell
- pixi add nbclassic
-->

# Review: pixi global

>- Installs packages in a global space
>- Always available
>- Good options for CLI tools

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

>- We can add packages to our project
>- We can add/remove as we go, the env is re-solved and the lockfile refreshed.

# Review: pixi lockfile

>- Ensure the exact same version, same package, is used when re-creating the environment.


# Review: pixi as conda alternative

```
pixi shell
```

Will "activate" a conda-like environment.

# What about the [tasks] field?

Let's add a task that will run that notebook for us:

```toml
map = "jupyter nbconvert --to notebook --execute gliders_of_the_day.ipynb --output=gliders_of_the_day-output.ipynb"
```

# Using pixi run as a makefile

```toml
serve = { cmd = "cd html && python3 -m http.server 8080", depends-on = ["map"] }
```

# Some extra commands that we should know

>- `pixi tree`
>- `pixi list`
>- `pixi update`

# Please check the Docs

[https://pixi.sh/latest/](https://pixi.sh/latest/)

# Questions?

![](images/stromatolites.png)
