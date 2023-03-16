<!--
SPDX-FileCopyrightText: 2021 Bernardo Chrispim Baron <bc.bernardo@hotmail.com>

SPDX-License-Identifier: MIT
-->

# aw-watcher-ask

An [ActivityWatch][] watcher to pose questions to the user and record her
answers.

This watcher uses [Zenity][Zenity Manual] to present dialog boxes to the user, and stores her answers in a locally running instance of ActivityWatch. This can be useful to poll all sorts of information on a periodical or random basis. The inspiration comes from the [experience sampling method (ESM)](https://en.wikipedia.org/wiki/Experience_sampling_method) used in psychological studies, as well as from the [quantified self](https://en.wikipedia.org/wiki/Quantified_self) movement.

[ActivityWatch]: https://activitywatch.readthedocs.io/en/latest/

## Table of Contents

- [aw-watcher-ask](#aw-watcher-ask)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
    - [Using `pip`/`pipx`](#using-pippipx)
    - [From source](#from-source)
  - [Usage](#usage)
    - [CLI](#cli)
    - [Accessing the data](#accessing-the-data)
  - [Security](#security)
  - [Limitations and Roadmap](#limitations-and-roadmap)
  - [Maintainers](#maintainers)
  - [Contributing](#contributing)
  - [License](#license)

## Install

### Using `pip`/`pipx`

Create a [virtual environment][venv], activate it and run:

```sh
$ python3 -m pip install git+https://github.com/bcbernardo/aw-watcher-ask.git
Collecting git+https://github.com/bcbernardo/aw-watcher-ask.git
... ...
Installing collected packages: aw-watcher-ask
Successfully installed aw-watcher-ask-0.1.0
```

Alternatively, you may use [`pipx`][pipx] to abstract away the creation of the virtual environment, and make sure the package is globally available:

```sh
$ pipx install git+https://github.com/bcbernardo/aw-watcher-ask.git
  installed package aw-watcher-ask 0.1.0, Python 3.9.6
  These apps are now globally available
    - aw-watcher-ask
done! ✨ 🌟 ✨
```

[venv]: https://docs.python.org/3/tutorial/venv.html
[pipx]: https://pypa.github.io/pipx/

### From source

To install the watcher, clone the repository to your local filesystem and
install it with [poetry](https://python-poetry.org/docs):

```sh
$ git clone https://github.com/bcbernardo/aw-watcher-ask.git
$ cd aw-watcher-ask
$ poetry install
... ...
Installing the current project: aw-watcher-ask (0.1.0)
$ poetry shell  # alternatively, add `poetry run` before every command in the examples below
```

## Usage

Before you start using `aw-watcher-ask`, make sure you have ActivityWatch [installed and running][AW installation].

[AW installation]: https://docs.activitywatch.net/en/latest/getting-started.html

### CLI

The following command will show the dialog box below each hour at 00 minutes
and 00 seconds, wait up to 120 seconds for the user's response, and save it to
a bucket in the local ActivityWatcher instance.

```sh
$ aw-watcher-ask run --question-id "happiness.level" --question-type="question" --title="My happiness level" --text="Are you feeling happy right now?" --timeout=120 --schedule "0 */1 * * * 0"
... ...
```

![Example dialog asking if the user is happy](./assets/img/example_dialog.png)

Check `aw-watcher-ask run --help` to see all required and optional control parameters.

The `--question-id` is used to identify this particular question in the ActivityWatcher a `aw-watcher-ask` bucket, and is therefore mandatory.

The `question-type` parameters is also required and should be one of Zenity's supported [dialog types][Zenity Manual] (complex types such as `forms`, `file-selection` and `list` have not been implemented yet). All options supported by these dialog types are accepted by `aw-watcher-ask run` as extra parameters, and passed unaltered to Zenity under the hood.

[Zenity Manual]: https://help.gnome.org/users/zenity/stable/

### Accessing the data

All data gathered is stored under `aw-watcher-ask_localhost.localdomain` bucket (or `test-aw-watcher-ask_localhost.localdomain`, when running with the `--testing` flag) in the local ActivityWatch endpoint. Check ActivityWatch [REST API documentation][AW API] to learn how to get the stored events programatically, so that you can apply some custom analysis.

[AW API]: https://docs.activitywatch.net/en/latest/api/rest.html

## Security

As other ActivityWatcher [watchers][AW watchers], `aw-watcher-ask` communicates solely with the locally running AW server instance. All data collected is stored in your machine.

[AW watchers]: https://docs.activitywatch.net/en/latest/watchers.html

## Limitations and Roadmap

`aw-watcher-ask` is in a very early development stage. Expect bugs and strange behaviors when using it.

This package uses `zenity` utility, which must be installed in the system and globally accessible through the command line. Zenity comes pre-installed with most Linux installations, and can be installed from all major package repositories (`apt`, `dnf`, `pacman`, `brew` etc.).

Porting Zenity to Windows is not trivial. If you use Windows, you may give @ncruces' [Go port](https://github.com/ncruces/zenity) a shot, as it is supposed to be cross-platform. Instructions to install on Windows can be found [here](https://timing.rbind.io/post/2021-12-19-setting-up-zenity-with-windows-python-go/)

`aw-watcher-ask` does not currently have a way of storing the questions made, and scheduling them every time the system restarts. We want to implement this eventually, but for now you should wrap all questions you want to schedule in a (shell) script and configure your system to execute it at every startup.

## Maintainers

- Bernardo Chrispim Baron ([@bcbernardo](https://github.com/bcbernardo))

## Contributing

PRs accepted. Please [open an issue][new issue] if you have an idea for enhancement or have spotted a bug.

[new issue]: https://github.com/bcbernardo/aw-watcher-ask/issues/new/choose

## License

MIT License

Copyright (c) 2021 Bernardo Chrispim Baron

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
