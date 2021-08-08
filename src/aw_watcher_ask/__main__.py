#!/usr/bin/env python
#
# SPDX-FileCopyrightText: Bernardo Chrispim Baron <bc.bernardo@hotmail.com>
#
# SPDX-License-Identifier: MIT


"""Main entrypoint to aw-watcher ask."""


from aw_watcher_ask.cli import app


if __name__ == "__main__":
    app(prog_name="aw-input-watcher")
